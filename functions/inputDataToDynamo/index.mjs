import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocumentClient,PutCommand } from "@aws-sdk/lib-dynamodb";
import { v4 as uuidv4 } from 'uuid';

const client = new DynamoDBClient({});
const dynamo = DynamoDBDocumentClient.from(client);
const tableName = "data";

export const handler = async (event, context) => {
  try{
    const data = JSON.parse(event.Records[0].body)
    console.log(data.user, data.extractedData)
    await dynamo.send(
      new PutCommand({
        TableName: tableName,
        Item: {
          id: uuidv4(),
          user: data.user,
          data: JSON.stringify(data.extractedData),
          message: data.message
        },
      })
    );
  } catch(err) {
    console.log(err)
  }
}