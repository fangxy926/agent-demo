import requests
import json


def convert_swagger_to_openapi(swagger_url: str, path_key: str = None, max_paths: int = 100):
    # 读取Swagger 2文档
    response = requests.get(swagger_url)
    if response.status_code != 200:
        raise Exception(f"无法访问Swagger文档，HTTP状态码: {response.status_code}")

    swagger_doc = response.json()

    # 转换Swagger 2到OpenAPI 3
    openapi_doc = {
        "openapi": "3.0.0",
        "info": {
            "title": swagger_doc.get("info", {}).get("title", "API Documentation"),
            "description": swagger_doc.get("info", {}).get("description", ""),
            "version": swagger_doc.get("info", {}).get("version", "1.0.0")
        },
        "servers": {},
        "paths": {},
        "components": {
            "schemas": {},
            "securitySchemes": {}
        }
    }

    # 处理服务器信息
    if "host" in swagger_doc and "basePath" in swagger_doc:
        servers = [{
            "url": f"{swagger_doc.get('schemes', ['http'])[0]}://{swagger_doc['host']}{swagger_doc['basePath']}",
            "description": "API server"
        }]
        openapi_doc["servers"] = servers

    path_list = list(swagger_doc.get("paths", {}).items())[:max_paths]
    if path_key:
        path_list = [path_item for path_item in path_list if path_key in path_item[0]]
    # 转换Paths
    for path, path_item in path_list:
        openapi_doc["paths"][path] = {}
        for method, operation in path_item.items():
            operation_id = path.split("/")[-1].replace("{", "").replace("}", "")
            openapi_doc["paths"][path][method] = {
                # "summary": operation.get("summary", ""),
                "description": operation.get("description", ""),
                "operationId": operation_id,  # operation.get("operationId", ""),
                "parameters": [],
                "responses": {}
            }

            # 转换参数
            for param in operation.get("parameters", []):
                openapi_param = {
                    "name": param.get("name"),
                    "in": param.get("in"),
                    "description": param.get("description", ""),
                    "required": param.get("required", False)
                }

                if '$ref' in param.get('schema', {}):
                    # 处理引用类型的参数
                    ref = param['schema']['$ref']
                    ref_name = ref.split("/")[-1]  # 提取引用的类型名称
                    openapi_param["$ref"] = f"#/components/schemas/{ref_name}"
                else:
                    # 处理普通类型参数
                    openapi_param["schema"] = {
                        "type": param.get("type", "string")  # 默认使用string类型
                    }

                openapi_doc["paths"][path][method]["parameters"].append(openapi_param)

            # # 转换响应
            # for code, response in operation.get("responses", {}).items():
            #     openapi_doc["paths"][path][method]["responses"][code] = {
            #         "description": response.get("description", ""),
            #         "content": {
            #             "application/json": {
            #                 "schema": {
            #                     "type": "object"  # 默认使用object类型
            #                 }
            #             }
            #         }
            #     }

    # 转换Schemas（模型）
    if "definitions" in swagger_doc:
        for schema_name, schema in swagger_doc["definitions"].items():
            openapi_doc["components"]["schemas"][schema_name] = schema

    # 转换Security Schemes
    if "securityDefinitions" in swagger_doc:
        for security_name, security in swagger_doc["securityDefinitions"].items():
            openapi_doc["components"]["securitySchemes"][security_name] = security

    # 输出OpenAPI 3文档
    return json.dumps(openapi_doc, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    # 示例使用
    swagger_url = "http://10.104.141.231:38081/app-wyyycode/v2/api-docs"  # 替换为Swagger 2文档链接
    openapi_doc = convert_swagger_to_openapi(swagger_url, path_key="department", max_paths=100)
    # 保存到本地目录
    with open("openapi_doc.json", "w", encoding="utf-8") as f:
        f.write(openapi_doc)
