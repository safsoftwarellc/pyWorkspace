s = "/FpML/header/message-Id - messageId"

print((s.split('-')[1]).strip())
print(s.rfind('-'))
print(s[25:].strip())
print(s[:24].strip())
