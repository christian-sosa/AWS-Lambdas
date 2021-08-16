import json
import boto3
import os
from datetime import datetime, timedelta

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # TODO implement
    date = datetime.now()
    new_date = date.strftime("%d%m%Y")
    # parametros
    numero = str(event["queryStringParameters"]['numero'])
    nombre = event["queryStringParameters"]['nombre']

    #datos buckets y direcciones
    NombreBucket = 'NombreBucket'
    keyPut = 'Direccion'
    keyPutBackup = 'Direccion'+' '+new_date+'.json'
    print(keyPutBackup)
    keyGet = 'Direccion'
    #leo s3
    datos = s3.get_object(Bucket=NombreBucket, Key=keyGet)
    datosbien = datos['Body'].read().decode('utf-8')
    x = json.loads(datosbien)
    
    #transformo la data
    resultado = addProvedor(x,numero,nombre)
    y = json.dumps(resultado)
    #subo la data
    response = s3.put_object(Body=y,Bucket=NombreBucket, Key=keyPut)
    response2 = s3.put_object(Body=datosbien,Bucket=NombreBucket, Key=keyPutBackup)
    
    return {
       'statusCode': 200,
       "body": "{'message': ok}",
       'headers': { 'Content-Type': 'application/json' },
    }


def addProvedor (lista, numero, nombre) :
    newProvedor = [numero, nombre];
    lista["tramite"]["datos"][7]["proveedores"].append(newProvedor);
    return lista

