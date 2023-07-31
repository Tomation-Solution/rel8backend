from django.test import TestCase

# Create your tests here.
a =     {"id":4495436,"txRef":"bkgqgvsyihqcfnazqzxm","flwRef":"FLW-M03K-43ed0d520e053b20d3e9d03dd80d95e5","orderRef":"URF_BA8FB9F67FCD6D68DB_4391779",
"paymentPlan":'null',"paymentPage":'null',"createdAt":"2023-07-31T00:46:31.000Z","amount":1000,
"charged_amount":1000,"status":"successful","IP":"52.209.154.143","currency":"NGN","appfee":38,
"merchantfee":0,"merchantbearsfee":1,"customer":{"id":2161085,"phone":"2348162047348","fullName":"Markothedev ",
"customertoken":'null',"email":"test@gmail.com","createdAt":"2023-07-31T00:45:15.000Z",
"updatedAt":"2023-07-31T00:45:15.000Z","deletedAt":'null',"AccountId":2139517},"entity":
{"card6":"417396","card_last4":"4708","card_country_iso":"IQ","createdAt":"2023-07-31T00:31:48.000Z"},"event.type":"CARD_TRANSACTION"}

print(a.get('status'))