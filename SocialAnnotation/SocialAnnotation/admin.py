from io import BytesIO
import zipfile
from io import StringIO
import json
import datetime
from django.contrib import admin
from django.http import HttpResponse
from .models import SocialAnnotation

admin.site.site_title = 'SocialAnnotation admin'
admin.site.site_header = 'SocialAnnotation データ管理'
admin.site.index_title = 'データ管理'


class SocialAnnotationDisplay(admin.ModelAdmin):
    list_display = ("hypothesis_url", "hypothesis_text", "annotation_type", "relevant_url", "id")


admin.site.register(SocialAnnotation, SocialAnnotationDisplay)
# def download_json(modeladmin, request, queryset):
#     memory_file = BytesIO()
#     zip_file = zipfile.ZipFile(memory_file, 'w')
#
#     for theme_obj in queryset:
#         filename = (theme_obj.theme_name + ".json")
#
#         json_data = {
#             "Theme": {
#                 "theme_id": theme_obj.id,
#                 "theme_name": theme_obj.theme_name,
#                 "theme_description": theme_obj.theme_description
#             },
#             "Node": {
#                 "nodes": [],
#                 "relevant_infos": [],
#                 "rootNode_id": NodeNode.objects.filter(parent_node__isnull=True, child_node__theme__id=theme_obj.id)[0]
#                     .child_node.id
#             },
#         }
#         json_node_data = json_data["Node"]
#         for node in theme_obj.nodes.all():
#             node_data = {
#                 "node_id": node.id,
#                 "node_name": node.node_name,
#                 "node_type": node.node_type,
#                 "node_description": node.node_description,
#                 "child_nodes_id": [],
#                 "relevant_infos_id": [],
#             }
#             json_node_data["nodes"].append(node_data)
#
#             for nodenode in node.parent.all():
#                 node_data["child_nodes_id"].append(nodenode.child_node.id)
#
#             for relevant_info in node.relevant_info.all():
#                 relevant_info_data = {
#                     "relevant_info_id": relevant_info.id,
#                     "relevant_info_url": relevant_info.relevant_url,
#                     "relevant_info_title": relevant_info.relevant_title
#                 }
#                 json_node_data["relevant_infos"].append(relevant_info_data)
#                 node_data["relevant_infos_id"].append(relevant_info.id)
#
#         json_data = json.dumps(json_data, ensure_ascii=False, indent='\t')
#         zip_file.writestr(zinfo_or_arcname=filename, data=json_data)
#
#     zip_file.close()
#     response = HttpResponse(memory_file.getvalue(), content_type='application/zip')
#     response['Content-Disposition'] = 'attachment; filename=IBIS_json-%s.zip' % datetime.date.today()
#     return response
#
#
# def download_ttl(modeladmin, request, queryset):
#     ttl_string = "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n" \
#                  "@prefix dct: <http://purl.org/dc/terms/> .\n\n"
#
#     ontology = ONTOLOGY
#     theme_resource_pref = LOD_RESOURCE + "themes/"
#     node_resource_pref = LOD_RESOURCE + "nodes/"
#     relevant_resource_pref = LOD_RESOURCE + "relevant_infos/"
#
#     def make_ibis_ontology(query):
#         return "<" + ontology + query + ">"
#
#     def convert_ttl(subject, predicate, object):
#         return subject + " " + predicate + " " + object + ". \n"
#
#     for theme in queryset:
#         theme_obj = "<" + theme_resource_pref + str(theme.id) + ">"
#         theme_name = '"' + theme.theme_name + '"@ja'
#         theme_description = '"""' + theme.theme_description + '"""@ja'
#         rootNode_id = NodeNode.objects.filter(parent_node__isnull=True, child_node__theme__id=theme.id)[0] \
#             .child_node.id
#         theme_rootNode = "<" + node_resource_pref + str(rootNode_id) + ">"
#
#         ttl_string += convert_ttl(theme_obj, "rdf:type", make_ibis_ontology("Theme")) + \
#                       convert_ttl(theme_obj, "dct:title", theme_name) + \
#                       convert_ttl(theme_obj, "dct:description", theme_description) + \
#                       convert_ttl(theme_obj, make_ibis_ontology("rootNode"), theme_rootNode) + "\n"
#
#         for node in theme.nodes.all():
#             node_obj = "<" + node_resource_pref + str(node.id) + ">"
#             node_name = '"' + node.node_name + '"@ja'
#             ttl_string += convert_ttl(node_obj, "rdf:type", make_ibis_ontology(node.node_type)) + \
#                           convert_ttl(node_obj, make_ibis_ontology("theme"), theme_obj) + \
#                           convert_ttl(node_obj, "dct:title", node_name)
#
#             node_description = node.node_description
#             if len(node_description.strip()) != 0:
#                 node_description = '"""' + node_description + '"""@ja'
#                 ttl_string += convert_ttl(node_obj, "dct:title", node_description)
#
#             for nodenode in node.parent.all():
#                 child_node_obj = "<" + node_resource_pref + str(nodenode.child_node.id) + ">"
#                 ttl_string += convert_ttl(child_node_obj, make_ibis_ontology("responseOf"), node_obj)
#
#             for relevant_info in node.relevant_info.all():
#                 relevant_info_obj = "<" + relevant_resource_pref + str(relevant_info.id) + ">"
#                 relevant_url = '<' + relevant_info.relevant_url + '>'
#                 relevant_title = '"' + relevant_info.relevant_title + '"@ja'
#
#                 ttl_string += convert_ttl(node_obj, make_ibis_ontology("relevant"), relevant_info_obj) + \
#                               convert_ttl(relevant_info_obj, "rdf:type", make_ibis_ontology("RelevantInfo")) + \
#                               convert_ttl(relevant_info_obj, "dct:title", relevant_title) + \
#                               convert_ttl(relevant_info_obj, make_ibis_ontology("relatedURL"), relevant_url) + \
#                               convert_ttl(relevant_info_obj, make_ibis_ontology("node"), node_obj)
#
#     file = StringIO()
#     file.write(ttl_string)
#     response = HttpResponse(file.getvalue(), content_type="text/turtle")
#     response['Content-Disposition'] = 'attachment; filename=IBIS_creator-%s.ttl' % datetime.date.today()
#     file.close()
#     return response
#
# download_json.short_description = "download IBIS's as json format file"
# download_ttl.short_description = "download IBIS as Turtle format file"

