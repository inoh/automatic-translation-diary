from aws_cdk import (core,
                     aws_lambda,
                     aws_apigatewayv2,
                     aws_dynamodb)


class AutomaticTranslationDiaryStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        pages_dynamodb_table = aws_dynamodb.Table(self, 'Pages',
            partition_key=aws_dynamodb.Attribute(
                name='id',
                type=aws_dynamodb.AttributeType.STRING)
        )

        api = aws_apigatewayv2.HttpApi(
            self, id, api_name='AutomaticTranslationDiary',
            cors_preflight=aws_apigatewayv2.CorsPreflightOptions(
                allow_headers=['Content-Type'],
                allow_methods=[
                    aws_apigatewayv2.HttpMethod.GET,
                    aws_apigatewayv2.HttpMethod.POST,
                    aws_apigatewayv2.HttpMethod.OPTIONS
                ],
                allow_origins=['*'],
            ),
        )

        def add_routes(endpoint, handler):
            method, path = endpoint.split(' ')

            function = aws_lambda.Function(
                self, handler.replace('.', '-'),
                runtime=aws_lambda.Runtime.PYTHON_3_8,
                code=aws_lambda.Code.asset('lambda/src'),
                handler=handler)

            pages_dynamodb_table.grant_read_write_data(function)
            function.add_environment(
                'DYNAMODB_NAME_PAGES',
                pages_dynamodb_table.table_name)

            integration = aws_apigatewayv2.LambdaProxyIntegration(handler=function)

            api.add_routes(
                path=path,
                methods=[aws_apigatewayv2.HttpMethod[method]],
                integration=integration)


        add_routes('POST /diaries', 'diary_handler.save')
        add_routes('GET /diaries', 'diary_handler.diaries')
        add_routes('GET /diaries/{diaryId}/{lang}', 'page_handler.page')
