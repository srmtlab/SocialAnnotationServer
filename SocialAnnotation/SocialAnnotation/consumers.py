import json
import requests
import re
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import SocialAnnotation


class SocialAnnotationConsumer(WebsocketConsumer):
    def connect(self):
        self.theme_name = 'index'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.theme_name,
            self.channel_name
        )

        self.accept()

    def get_hypothesis_text(self, hypothesis_url):

        pattern = 'https?://hyp.is/(.*?)(?=/)'
        repatter = re.compile(pattern)
        result = repatter.match(hypothesis_url)

        url = "https://api.hypothes.is/api/annotations/" + result[1]

        headers = {
            'authorization': "Bearer 6879-5xKEqgNrOAhD3-ak-K0_zo_KRJ5YK6qV6c53d5jiHm4",
        }

        response = requests.request("GET", url, headers=headers)

        if response.status_code == 200:
            text_data_json = json.loads(response.text)
            for selector in text_data_json["target"][0]["selector"]:
                if selector["type"] == "TextQuoteSelector":
                    return selector["exact"]
        else:
            return False


    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.theme_name,
            self.channel_name
        )

    def renew_database(self, data_operation, data):
        if data_operation == "add":
            try:
                hypothesis_url = data['hypothesis_url']
                hypothesis_text = "test Text"
                annotation_type = data['annotation_type']
                relevant_url = data['relevant_url']
            except KeyError:
                return False
            else:
                SocialAnnotation_obj = SocialAnnotation(
                    hypothesis_url = hypothesis_url,
                    hypothesis_text = hypothesis_text,
                    annotation_type = annotation_type,
                    relevant_url = relevant_url
                )
                SocialAnnotation_obj.save()
                data['hypothesis_text'] = hypothesis_text
                data['annotation_id'] = SocialAnnotation_obj.id
                return True
        elif data_operation == "delete":
            annotation_id  = int(data["annotation_id"])
            SocialAnnotation.objects.filter(pk=annotation_id).delete()
            return True
        elif data_operation == "edit":
            try:
                annotation_id = int(data["annotation_id"])
                annotation_type = data['annotation_type']
                relevant_url = data['relevant_url']
            except (KeyError, ValueError):
                return False
            else:
                try:
                    SocialAnnotation_obj = SocialAnnotation.objects.get(pk=annotation_id)
                    SocialAnnotation_obj.annotation_type = annotation_type
                    SocialAnnotation_obj.relevant_url = relevant_url
                    SocialAnnotation_obj.save()
                    return True
                except SocialAnnotation.DoesNotExist:
                    return False

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        try:
            status = text_data_json['status']
        except KeyError:
            pass
        else:
            if status == "init":
                try:
                    socialannotations = SocialAnnotation.objects.all().order_by('id').reverse()
                except SocialAnnotation.DoesNotExist:
                    pass
                else:
                    socialannotation_list = []
                    for annotation in socialannotations:
                        annotation = {
                            'annotation_id': annotation.id,
                            'hypothesis_url': annotation.hypothesis_url,
                            'hypothesis_text': annotation.hypothesis_text,
                            'annotation_type': annotation.annotation_type,
                            'relevant_url': annotation.relevant_url
                        }
                        socialannotation_list.append(annotation)

                    # クライアントが，WebSocket通信を始めた瞬間であれば
                    async_to_sync(self.channel_layer.group_send)(
                        self.theme_name,
                        {
                            'type': 'send_annotation',
                            'send_data': {
                                'status': 'init',
                                'data': socialannotation_list
                            }
                        }
                    )
            elif status == "work":
                try:
                    data_operation = text_data_json["operation"]
                    data = text_data_json["data"]
                except KeyError:
                    pass
                else:
                    save_flag = self.renew_database(data_operation=data_operation, data=data)
                    if save_flag:
                        async_to_sync(self.channel_layer.group_send)(
                            self.theme_name,
                            {
                                'type': 'send_annotation',
                                'send_data': {
                                    'status': 'work',
                                    'operation': data_operation,
                                    'data': data
                                }
                            }
                        )

    def send_annotation(self, event):
        self.send(text_data=json.dumps(event['send_data']))
