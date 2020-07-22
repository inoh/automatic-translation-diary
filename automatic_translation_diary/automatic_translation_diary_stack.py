from aws_cdk import (core, aws_lambda, aws_apigatewayv2)

class AutomaticTranslationDiaryStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

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

        handler = self.create_lambda_function(
            'SaveDiary',
            'diary_usecase.save')

        integration = aws_apigatewayv2.LambdaProxyIntegration(handler=handler)

        api.add_routes(
            path='/diaries',
            methods=[aws_apigatewayv2.HttpMethod.POST],
            integration=integration)


    def create_lambda_function(self, name, handler):
        return aws_lambda.Function(
            self, f'AutomaticTranslationDiary{name}',
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            code=aws_lambda.Code.asset('lambda'),
            handler=handler)
