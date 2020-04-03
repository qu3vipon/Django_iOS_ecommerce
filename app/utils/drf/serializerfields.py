from phonenumber_field.serializerfields import PhoneNumberField as DefaultPhoneNumberField


class PhoneNumberField(DefaultPhoneNumberField):
    def to_representation(self, value):
        if hasattr(value, 'as_national'):
            return value.as_national
        return value
