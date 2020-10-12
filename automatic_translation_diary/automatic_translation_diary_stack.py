from aws_cdk import (core,
                     aws_iam,
                     aws_lambda,
                     aws_apigatewayv2,
                     aws_dynamodb)
from aws_cdk.aws_lambda_event_sources import DynamoEventSource


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

        def create_function(handler: str):
            function = aws_lambda.Function(
                self, handler.replace('.', '-'),
                runtime=aws_lambda.Runtime.PYTHON_3_8,
                code=aws_lambda.Code.asset('lambda/src'),
                handler=handler)

            pages_dynamodb_table.grant_read_write_data(function)
            function.add_environment(
                'DYNAMODB_NAME_PAGES',
                pages_dynamodb_table.table_name)
            function.add_to_role_policy(
                aws_iam.PolicyStatement(
                    resources=['*'],
                    actions=['translate:TranslateText', 'polly:SynthesizeSpeech']))

            return function

        api.add_routes(
            path='/diaries',
            methods=[aws_apigatewayv2.HttpMethod.POST],
            integration=aws_apigatewayv2.LambdaProxyIntegration(
                handler=create_function('diary_handler.save')
            ))

        api.add_routes(
            path='/diaries',
            methods=[aws_apigatewayv2.HttpMethod.GET],
            integration=aws_apigatewayv2.LambdaProxyIntegration(
                handler=create_function('diary_handler.diaries')
            ))

        api.add_routes(
            path='/diaries/{diaryId}/{lang}',
            methods=[aws_apigatewayv2.HttpMethod.GET],
            integration=aws_apigatewayv2.LambdaProxyIntegration(
                handler=create_function('page_handler.page')
            ))

        api.add_routes(
            path='/diaries/{diaryId}/{lang}/speech',
            methods=[aws_apigatewayv2.HttpMethod.GET],
            integration=aws_apigatewayv2.LambdaProxyIntegration(
                handler=create_function('page_handler.speech')
            ))
