# 1. Tổng quan quy trình
Đoạn mã thực hiện bài toán phân loại nhị phân (Binary Classification) nhằm dự đoán khả năng sống sót (Survived: 0 hoặc 1) của hành khách trên tàu Titanic dựa trên các thông tin cá nhân và đặc điểm vé

# 2. Phân tích nội dung thực hành & Lý thuyết áp dụng
Đọc và duyệt cấu trúc dữ liệu:
Tự động xác định đường dẫn thư mục lưu trữ và tải hai tập dữ liệu: tập huấn luyện (train.csv) và tập kiểm thử (test.csv)

Khám phá và trực quan hóa dữ liệu (EDA):
Phân tích phân bố: Phân tích tần suất và tỷ lệ sống sót theo từng nhóm thuộc tính như hạng vé (Pclass), độ tuổi (Age), giá vé (Fare) và số lượng người thân đi cùng (SibSp)

Chẩn đoán dữ liệu thiếu (Missing Values): Sử dụng biểu đồ nhiệt (Heatmap) và thống kê giá trị NULL để xác định mức độ thiếu hụt dữ liệu trên các thuộc tính

Phân tích tương quan: Quan sát sự phân bố độ tuổi tương ứng với từng hạng vé bằng biểu đồ hộp (Boxplot)

Tiền xử lý dữ liệu (Data Preprocessing):
Mã hóa biến phân loại (One-Hot Encoding): Chuyển đổi các biến định tính (Sex, Embarked, Pclass) thành các biến giả dạng số (0 và 1) bằng phương pháp One-Hot Encoding với thuộc tính loại bỏ cột đầu tiên (drop_first=True) nhằm loại bỏ hiện tượng đa cộng tuyến (Dummy Variable Trap)

Xử lý giá trị khuyết (Data Imputation): Thay thế các vị trí dữ liệu thiếu ở biến độ tuổi (Age) và giá vé (Fare) bằng giá trị trung bình (mean) của thuộc tính đó

Loại bỏ đặc trưng dư thừa (Feature Selection): Bỏ các thuộc tính định danh, chuỗi văn bản không đóng góp trực tiếp vào mô hình phân loại (như PassengerId, Name, Ticket, Cabin và các cột định tính gốc)

Huấn luyện và đánh giá mô hình:
Phân chia dữ liệu: Tách tập huấn luyện ban đầu thành 2 phần theo tỷ lệ 70% để huấn luyện và 30% để kiểm thử mô hình

Thuật toán Hồi quy Logistic (Logistic Regression): Sử dụng mô hình Hồi quy Logistic với bộ giải liblinear — thuật toán tối ưu hóa thích hợp cho bài toán phân loại nhị phân trên tập dữ liệu nhỏ

Đánh giá hiệu năng: Kiểm tra chất lượng mô hình thông qua 3 chỉ số chính

Accuracy Score: Độ chính xác tổng thể của các dự đoán

Confusion Matrix (Ma trận nhầm lẫn): Thống kê số lượng bản ghi dự đoán đúng và sai đối với từng lớp (Sống sót / Không sống sót)

Classification Report: Báo cáo chi tiết các độ đo Precision, Recall và F1-score

# Dự đoán và xuất kết quả:
Áp dụng mô hình đã huấn luyện lên tập dữ liệu test độc lập và lưu file kết quả submission.csv chứa mã hành khách cùng dự đoán sống sót tương ứng

