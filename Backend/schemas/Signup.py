from pydantic import (
    BaseModel,
    EmailStr,
    field_validator,
    model_validator
)


class Signup(BaseModel):
    full_name: str
    Email_Address: EmailStr
    Password: str
    Confirm_password: str

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, v):

        if not v.strip():
            raise ValueError("Full name cannot be empty")

        return v.strip()

    @field_validator("Password")
    @classmethod
    def validate_password(cls, v):

        if len(v) < 8:
            raise ValueError(
                "Password must be at least 8 characters"
            )

        return v

    @model_validator(mode="after")
    def passwords_match(self):

        if self.Password != self.Confirm_password:
            raise ValueError("Passwords do not match")

        return self
    
