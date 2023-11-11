
"""
Convert Arabic Number to Roman Number.
เขียนโปรแกรมรับค่าจาก user เพื่อแปลง input ของ user ที่เป็นตัวเลขอราบิก เป็นตัวเลขโรมัน
โดยที่ค่าที่รับต้องมีค่ามากกว่า 0 จนถึง 1000

*** อนุญาตให้ใช้แค่ตัวแปรพื้นฐาน, built-in methods ของตัวแปรและ function พื้นฐานของ Python เท่านั้น
ห้ามใช้ Library อื่น ๆ ที่ต้อง import ในการทำงาน(ยกเว้น ใช้เพื่อการ test การทำงานของฟังก์ชัน).

"""
def convert_roman(number):
    #เช็คว่ามีค่ามากกว่า 0 จนถึง 1000
    if(number>1000 or number<=0):
        return "input out of range"
    result = ""
    roman_data = [["M",1000],["D",500],["C",100],["L",50],["X",10],["V",5],["I",1]]

    for i in range(0,len(roman_data),2):
        n = number//roman_data[i][1]
        if(n>0):
            if(n==9):
                result += roman_data[i][0] + roman_data[i-2][0]
            elif(n==5):
                result += roman_data[i-1][0]
                number -= roman_data[i-1][1]   
            elif(n>5):
                result += roman_data[i-1][0] + (roman_data[i][0] * (n-5))
                number -= roman_data[i-1][1] + (roman_data[i][1] * (n-5))
            elif(n==4):
                result += roman_data[i][0] + roman_data[i-1][0] 
            else:
                result += roman_data[i][0] * n
            number = number%roman_data[i][1]

    return result

input_number = int(input("input : ")) 
print(convert_roman(input_number))  