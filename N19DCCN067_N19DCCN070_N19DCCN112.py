"""
N19DCCN067 - Ngô Sơn Hồng
N19DCCN070 - Lê Quang Hùng
N19DCCN112 - Nguyễn Thị Huỳnh My
"""
import math
import time
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from bisect import bisect_left

def binary_search(sorted_list, target):
    index = bisect_left(sorted_list, target)
    if index < len(sorted_list) and sorted_list[index] == target:
        return index
    return -1
def doc_file_set(duong_dan):
    with open(duong_dan, 'r') as file:
        noi_dung_file = file.read()
    noi_dung_file = noi_dung_file.lower()
    # print(noi_dung_file)
    stop_words = set(stopwords.words('english'))

    bat_dau_cau_moi = 0
    id = []
    noi_dung_stop_word = []
    for i in range(0, len(noi_dung_file)):
        if noi_dung_file[i] == "/":
            id.append(noi_dung_file[bat_dau_cau_moi:i].split()[0])
            noi_dung = set(noi_dung_file[bat_dau_cau_moi:i].split()[1:])
            bat_dau_cau_moi = i + 1
            noi_dung_stop_word.append([w for w in noi_dung if not w.lower() in stop_words])

    return noi_dung_stop_word, id
def doc_file_list(duong_dan):
    with open(duong_dan, 'r') as file:
        noi_dung_file = file.read()
    noi_dung_file = noi_dung_file.lower()
    # print(noi_dung_file)
    stop_words = set(stopwords.words('english'))

    bat_dau_cau_moi = 0
    id = []
    noi_dung_stop_word = []
    for i in range(0, len(noi_dung_file)):
        if noi_dung_file[i] == "/":
            id.append(noi_dung_file[bat_dau_cau_moi:i].split()[0])
            noi_dung = list(noi_dung_file[bat_dau_cau_moi:i].split()[1:])
            bat_dau_cau_moi = i + 1
            noi_dung_stop_word.append([w for w in noi_dung if not w.lower() in stop_words])

    return noi_dung_stop_word, id
def tao_list_tuple_tu_va_id(noi_dung_doc_text, id):
    tu_va_id = []
    for i in range(0, len(id)):
        for tu in noi_dung_doc_text[i]:
            tu_va_id.append((tu, id[i]))
    # print(tu_va_id)
    return sorted(tu_va_id, key=lambda x: x[0])
def tao_ds_tutansuatvitri(tu_va_id):
    i_vitri = 0
    tu_tansuat_vitri = []
    tan_suat_tu = 0
    tu_previuos =""
    for i in tu_va_id:
        if i[0] != tu_previuos:
            tan_suat_tu = 1
            tu_tansuat_vitri.append((i[0], tan_suat_tu, i_vitri))
            i_vitri += 1
            tu_previuos = i[0]
        else:
            tan_suat_tu += 1
            tu_tansuat_vitri[i_vitri-1] = (i[0], tan_suat_tu, i_vitri-1)
       
    return tu_tansuat_vitri
def do_tuong_dong(tu_tansuat_vitri, noi_dung_doc_list , id_doc ,result_url , noi_dung_truy_van , id_truy_van ):
    f = open(result_url, "w")
    list_tu =[]
    for tu in tu_tansuat_vitri:
        list_tu.append(tu[0])
    for i_tv in range(0,len(id_truy_van)):
        f.write(str(id_truy_van[i_tv]) + "\n")
        max_cos = 0
        max_cos_doc = 0
        for i_doc in range(0,len(id_doc)):
            cos = 0
            giao_doc_query=[]
            giao_doc_query = list(set(noi_dung_doc_list[i_doc]) & set(noi_dung_truy_van[i_tv]))
            for tu_in_giao in giao_doc_query:
                index =binary_search(list_tu,tu_in_giao)
                count_doc = noi_dung_doc_list[i_doc].count(tu_tansuat_vitri[index][0])
                count_truy_van = noi_dung_truy_van[i_tv].count(tu_tansuat_vitri[index][0])

                tf_doc = 1 + math.log10(count_doc)
                tf_truyvan = 1 + math.log10(count_truy_van)
                cos = cos + tf_doc* tf_truyvan*math.log10(
                    int(id_doc[-1])/int(tu_tansuat_vitri[index][1])) * math.log10(
                    int(id_doc[-1])/int(tu_tansuat_vitri[index][1]))
            f.write(str(i_doc) + ":" + str(round(cos,2)) + " ")
            if (cos > max_cos): 
                max_cos = cos
                max_cos_doc = i_doc
        f.write("\n" + "Do tuong dong lon nhat - ID DOC: " + str(max_cos_doc) + "  Cos_value: " + str(round(max_cos,2)) + "\n"
                + "  \   " + "\n")
    f.close() 
def ghi_file_tu_tansat_vitri(tu_tansaut_vitri_url ,tu_tansuat_vitri ):
    f = open(tu_tansaut_vitri_url, "w")
    for tu in tu_tansuat_vitri:
        string = str(tu[0]) + " " + str(tu[1]) + " " + str(tu[2]) + "\n"
        f.write(string)
    f.close()

def ghi_file_chi_muc_nguoc(chi_muc_nguoc_url ,chi_muc_nguoc ):
    f1 = open(chi_muc_nguoc_url, "w")
    for ids in chi_muc_nguoc:
        string = ""
        for i in range(0, len(ids)):
            if i == len(ids)-1:
                string += str(ids[i]) + "\n"
            else:
                string += str(ids[i]) + " "
        f1.write(string)
    f1.close()

if __name__ == '__main__':
    start_time = time.time()
    base_url = 'E:\A_OFFLINE_HK8\ChuyendeCNPM\IR2_CNPM'
    noidung_url = base_url + '//doc-text'
    truyvan_url = base_url + '//query-text'
    result_url = base_url + '//result_do_tuong_dong'
    tu_tansaut_vitri_url = base_url + '//tu_tansuat_vitri'
    print('Tách từ trong file doc-text tạo ds các từ không trùng nhau trong 1 doc')
    noi_dung_doc_set , id_doc_set = doc_file_set(noidung_url)


    print(".....")
    print('Tạo danh sách từ có trong file doc-text - sắp xếp')
    tu_va_id_doc = tao_list_tuple_tu_va_id(noi_dung_doc_set, id_doc_set)


    print(".....")
    print('Tạo danh sách bộ từ vựng và số doc nó xuất hiện (tansuat)')
    tu_tansuat_vitri = tao_ds_tutansuatvitri(tu_va_id_doc)
    # ghi_file_tu_tansat_vitri(tu_tansaut_vitri_url,tu_tansuat_vitri)


    print(".....")
    print('Tách các từ trong từng doc trong doc-text vẫn giữ các từ trùng trong 1 doc ')
    noi_dung_doc_list, id_doc_list = doc_file_list(noidung_url)


    print(".....")
    print('Tách từ trong danh sách query-text')
    noi_dung_truy_van_list, id_tv_list = doc_file_list(truyvan_url)


    print(".....")
    print('Đang tính độ tương đồng.......')
    do_tuong_dong(tu_tansuat_vitri , noi_dung_doc_list, id_doc_list, result_url ,noi_dung_truy_van_list,id_tv_list)
    
    print('Hoàn thành chương trình!')
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Thời gian chạy chương trình: {total_time} giây")

    
