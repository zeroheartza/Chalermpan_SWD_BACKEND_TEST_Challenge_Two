
"""
Convert Number to Thai Text.
เขียนโปรแกรมรับค่าจาก user เพื่อแปลง input ของ user ที่เป็นตัวเลข เป็นตัวหนังสือภาษาไทย
โดยที่ค่าที่รับต้องมีค่ามากกว่าหรือเท่ากับ 0 และน้อยกว่า 10 ล้าน

*** อนุญาตให้ใช้แค่ตัวแปรพื้นฐาน, built-in methods ของตัวแปรและ function พื้นฐานของ Python เท่านั้น
ห้ามใช้ Library อื่น ๆ ที่ต้อง import ในการทำงาน(ยกเว้น ใช้เพื่อการ test การทำงานของฟังก์ชัน).

"""
def convert_int_to_thai_char(number):
    #เช็คว่ามีค่ามากกว่าหรือเท่ากับ 0 และน้อยกว่า 10 ล้าน
    if(number>=10000000 or number<0):
        return "input out of range"
    n = 44 # ตัวอักษรไทยทั่งหมด 44 ตัว 
    result = []
    thai_char = ['ก', 'ข', 'ฃ', 'ค', 'ฅ', 'ฆ', 'ง', 'จ', 'ฉ', 'ช', 'ซ', 'ฌ', 'ญ', 'ฎ', 'ฏ', 'ฐ', 'ฑ', 'ฒ', 'ณ', 'ด', 'ต', 'ถ', 'ท', 'ธ', 'น', 'บ', 'ป', 'ผ', 'ฝ', 'พ', 'ฟ', 'ภ', 'ม', 'ย', 'ร', 'ฤ', 'ล', 'ฦ', 'ว', 'ศ', 'ษ', 'ส', 'ห', 'ฬ', 'อ', 'ฮ']
    #แปลงเป็นเลขฐาน44 และนำมาเทียบใน Arr เพื่อแปลงเป็นตัวอักษรไทย
    while(number > 0):
        result.append(thai_char[(number % n)])
        number = int(number / n)
    
    result.reverse()
    
    return ("".join(result))

user_number = int(input("input : "))
print(convert_int_to_thai_char(user_number))