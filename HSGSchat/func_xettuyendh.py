
a_bcd_rep1 = 10

# func signature
# def ten_ham(   đầu vào  args, kwargs  ):
#
#     xử lý / pass
#
#     return đầu ra / default None

# def ham(a, b, c, d=7, e="string gi do"):
#     # do
#
#
# ham(1,4,5)
# ham(1,4,6, "u", "aodhsodh") # đúng thứ tự của args
# ham(3,4,5, e="ok")

def nhap_chi_tieu():
    chitieu = False
    while True:
        chitieu_str = input("Nhap chi tieu tuyen sinh: ")
        if chitieu_str.isnumeric():
            chitieu = int(chitieu_str)
            break
        else:
            print("Mời nhập vào số đúng! Mời nhập lại")
    return chitieu

def input_sv():
    ten = input("Ten sv:")
    diem_tong_str = input("Nhap diem thi đh:")
    if diem_tong_str.isnumeric():
        diem_tong = float(diem_tong_str)
    else:
        diem_tong = None
    uu_tien = input("Y nếu ưu tiên, Khác để bỏ qua")
    is_uu_tien = True if uu_tien == "Y" else False
    return (ten, diem_tong, is_uu_tien)

def print_banner():
    print("Welcome to TSDH")
    # return
sv = [] # list
sv_uu_tien = []
def save(ten: str, diem=0) -> None: # arguments
    # ten ~ ten_sv ở dòng 40, diem ~ diem_thi dòng 40
    sv.append({"name": ten, "diem": diem})

def save_uu_tien(ten: str, diem: float) -> None:
    sv_uu_tien.append({"name": ten, "diem": diem})

chitieu = nhap_chi_tieu()


def luu_sv(save_func, *args, **kw): # luu_sv(save, ten, diem)
    # args ~ (ten, diem)
    print(kw) # if "diem" in kw: do abc( ... )
    save_func(*args, **kw)
    print(args[0])

for i in range(3):
    ten_sv, diem_thi, is_prio = input_sv()
    if not is_prio:
        luu_sv(save, ten_sv, diem=diem_thi) # kw = {"diem": diem_thi}
    else:
        luu_sv(save_uu_tien, ten_sv, diem_thi)

print(sv)
print(sv_uu_tien)
