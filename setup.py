import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="automatic_translation_diary",
    version="0.0.1",

    description="Automatic translation Diary",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="ino_h",

    package_dir={"": "automatic_translation_diary"},
    packages=setuptools.find_packages(where="automatic_translation_diary"),

    install_requires=[
        "aws-cdk.core==1.49.1",
        "aws-cdk.aws-lambda==1.49.1",
        "aws-cdk.aws-apigatewayv2==1.49.1",
        "aws-cdk.aws-dynamodb==1.49.1",
    ],

    python_requires=">=3.6",
)
