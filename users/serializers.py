from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

class UsersSerializers(serializers.ModelSerializer):
      class Meta:
            model = CustomUser # here we are instantiating or referencing the customUser model
            fields = ['full_name','email','password'] # here we are listing out the fields which we are going to add validation
            extra_kwargs = {'password': {'write_only': True}} # we added this line to make sure the password is  not returned back as response

      def validate(self, data): # this function is used to validate the password in here data contains the payload data from the frontend
            user = CustomUser(
                  full_name = data.get('full_name'),
                  email=data.get('email',''),
            ) # in this line we are getting the data of the full_name and email
            password = data.get('password') # in here we are getting the password value from the customuser model
            try:
                  validate_password(password=password, user=user) #this function is used to validate the password and usermodel values like full_name and email
            except DjangoValidationError as e:
                  error_messages = [str(msg) for msg in e.messages]
                  raise serializers.ValidationError(error_messages) # if there is any validation error this will get triggered

            return data #the data will get returned and passed to the next function 

      def create(self, validated_data): #this function is used to create a user in here validated_data contains the validated data
            user = CustomUser(
                  email = validated_data['email'],
                  full_name = validated_data['full_name']                
            ) # in here we get the values from the email and full_name
            user.set_password(validated_data['password'])  # in this line we are hashing the password
            user.save() # in here we are saving that particular user in the database
            return user 

