import json
import boto3
import os
from datetime import datetime, timedelta

s3 = boto3.client('s3')

def lambda_handler(event, context):
    #TODO implement
    date = datetime.now()
    new_date = date.strftime("%d%m%Y")
    # parametros
    RUT = str(event["queryStringParameters"]['numero'])
    nombre = event["queryStringParameters"]['nombre']
    CC = str(event["queryStringParameters"]['CC'])
    banco = event["queryStringParameters"]['banco']
    #validaciones de campos NULL
    banco = validarBanco(banco)
    CC = validarCC(CC)
    #datos buckets y direcciones
    NombreBucket = 'bucket'
    file = 'direccion'
    fileBackup = 'backup/direccion'+' '+new_date+'.json'
    #leo s3
    datos = s3.get_object(Bucket=NombreBucket, Key=file)
    datosOk = datos['Body'].read().decode('utf-8')
    datoFormateado = json.loads(datosOk)
    res = validar(datoFormateado, RUT)
    if res == 0:
        resultado = addProvedor (datoFormateado,RUT,nombre,CC,banco)
        datoFinal = json.dumps(resultado)
        #subo la data
        response2 = s3.put_object(Body=datosOk,Bucket=NombreBucket, Key=fileBackup)
        response = s3.put_object(Body=datoFinal,Bucket=NombreBucket, Key=file)
        return {
            'statusCode': 200,
            "body": "{'message': ok}",
            'headers': { 'Content-Type': 'application/json' },
        }
    return {
            'statusCode': 200,
            "body": "{'message': fail}",
          
    }


def addProvedor(lista, RUT, nombre, CC,banco) :
    newProvedor = [RUT, nombre, CC, banco]
    lista["tramite"]["datos"][0]["informacion_proveedores"].insert(-1,newProvedor);
    return lista
    
def validarBanco(banco):
    if banco == 'null':
        banco = 'N\/A'
    return banco

def validarCC(CC):
    if CC == 'null':
        CC = 'N\/A'
    return CC

def validar(lista, numero):
    aux = lista["tramite"]["datos"][0]["informacion_proveedores"]
    for i in aux:
        if numero == i[0]:
            result = 1
            return result
    result = 0
    return result
       