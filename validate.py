"""Validator Module"""
import re

def validate(data, regex):
    """Custom Validator"""
    return True if re.match(regex, data) else False

def validate_email(email: str):
    """Email Validator"""
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return validate(email, regex)

def validate_phone(phone: str):
    regex_phone = r'\b[\d]{3}[\d]{3}[\d]{4}\b'
    return validate(phone, regex_phone)

def validate_user(**args):
    """User Validator"""
    if  not args.get('email'):
        return {
            'email': 'Email is required',
        }
    if  not args.get('name'):
        return {
            'name': 'Name is required'
        }
    if  not args.get('age'):
        return {
            'age': 'age is required'
        }
    if  not args.get('dob'):
        return {
            'dob': 'dob is required'
        }
    if  not args.get('phone'):
        return {
            'phone': 'phone is required'
        }
    if not isinstance(args.get('name'), str) or \
        not isinstance(args.get('email'), str) or \
        not isinstance(args.get('dob'), str) or \
        not isinstance(args.get('phone'), str):
        return {
            'email': 'Email must be a string',
            'name': 'Name must be a string',
            'dob': 'dob must be a string',
            'phone': 'phone must be a string'
        }
    if not validate_email(args.get('email')):
        return {
            'email': 'Email is invalid'
        }
    if not validate_phone(args.get('phone')):
        return {
            'phone': 'Phone Number must be String and of 10 Digit'
        }
    return True