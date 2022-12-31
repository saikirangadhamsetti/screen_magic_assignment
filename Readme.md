The project was done using django
using models the data of csv fie was loaded into database
based on the methods the data sorted before saving into database
after saving to database "Messages",the data was retreived from it for sending the messages and emails
messages were sent using screen magic api and emails using django send email module
first the user is directed to add a .csv file when he entered the url "upload_csv/".
after adding the .csv file the data will be read in backend and get saved into database based on methods 
after uploading the .csv file user will be redirected to "textfile/" url there will be available a button for taking out a .txt file containing reports of message sending
the .txt file consists of entire message data and succcess status of the message
the data stored in database wil be used for sending messages and emails .After giving .txt response,the data wil be deleted.
