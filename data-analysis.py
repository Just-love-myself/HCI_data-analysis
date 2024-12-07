import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 답지 데이터 구조
answer_key = {
    "NUMBER": {
        3: ['2', '5', '8', '3', '4', '1', '9', '7', '6'],
        4: ['13', '16', '14', '5', '10', '6', '4', '7', '9', '12', '8', '3', '2', '15', '1', '11'],
        5: ['9', '14', '21', '24', '2', '10', '7', '15', '18', '25', '4', '11', '23', '22', '3', '20', '16', '19', '8', '12', '5', '6', '13', '1', '17']
    },
    "SHAPE": {
        3: ['□', '♤', '◇', '♥', '♬', '♪', '♣', '◆', '♦'],
        4: ['♫', '♬', '♦', '○', '●', '◀', '♣', '♡', '♤', '▲', '★', '◆', '♥', '▶', '☆', '△'],
        5: ['◀', '♩', '●', '☆', '◇', '♡', '▶', '♫', '♤', '△', '■', '◆', '▼', '♠', '□', '♣', '♢', '♧', '★', '♬', '♦', '▲', '○', '♪', '♥']
    },
    "ARABIC": {
        3: ['ا', 'ث', 'د', 'ع', 'ظ', 'ف', 'ن', 'ت', 'ص'],
        4: ['ع', 'ذ', 'ن', 'ط', 'ب', 'خ', 'ق', 'ج', 'م', 'ض', 'س', 'ك', 'ش', 'ل', 'ث', 'ت'],
        5: ['ظ', 'ف', 'ث', 'ض', 'س', 'ج', 'ت', 'ا', 'ر', 'ك', 'ب', 'ص', 'ن', 'خ', 'غ', 'ط', 'ق', 'م', 'ل', 'د', 'ش', 'ز', 'ع', 'ذ', 'ح']
    },
    "ALPHABET": {
        3: ['B', 'F', 'G', 'E', 'I', 'H', 'A', 'C', 'D'],
        4: ['I', 'A', 'C', 'D', 'F', 'M', 'L', 'E', 'J', 'O', 'G', 'P', 'B', 'H', 'N', 'K'],
        5: ['P', 'N', 'D', 'Y', 'O', 'W', 'A', 'R', 'X', 'F', 'J', 'M', 'B', 'H', 'T', 'I', 'Q', 'C', 'E', 'S', 'U', 'V', 'K', 'L', 'G']
    }
}

# Function to compare user answer with the answer key
def compare_answer(card_type, card_count, user_answer):
    correct_answer = answer_key.get(card_type, {}).get(card_count, None)
    if not correct_answer:
        raise ValueError(f"Invalid card_type '{card_type}' or card_count '{card_count}'")
    if len(user_answer) != len(correct_answer):
        raise ValueError("User answer length does not match the answer key length.")
    return [user == correct for user, correct in zip(user_answer, correct_answer)]

# Function to process and visualize user_answer as a grid
def plot_user_answer_grid(member_id, user_answer, card_type, card_count):
    correct_answer = answer_key.get(card_type, {}).get(card_count, None)
    if not correct_answer:
        raise ValueError(f"Invalid card_type '{card_type}' or card_count '{card_count}'")

    answer_list = user_answer.split(',')
    if len(answer_list) != len(correct_answer):
        print(f"Skipping mismatched answer for member_id={member_id}")
        return

    comparison = compare_answer(card_type, card_count, answer_list)

    grid_size = int(len(answer_list) ** 0.5)
    if grid_size ** 2 != len(answer_list):
        print(f"Skipping non-square user_answer for member_id={member_id}")
        return

    grid = np.array(answer_list).reshape((grid_size, grid_size))
    correct_grid = np.array(correct_answer).reshape((grid_size, grid_size))

    plt.figure(figsize=(6, 6))
    plt.title(f"Member ID: {member_id}, Card Type: {card_type}, Count: {card_count}")
    plt.imshow(np.zeros((grid_size, grid_size)), cmap="Blues", alpha=0.2)

    for i in range(grid_size):
        for j in range(grid_size):
            color = 'red' if not comparison[i * grid_size + j] else 'black'
            plt.text(j, i, grid[i, j], ha='center', va='center', fontsize=12, color=color, weight='bold')

    plt.xticks([])
    plt.yticks([])
    plt.show()


plt.close('all')
plt.clf()

# Load the Excel file
file_path = "C:/Users/DogyunKim/Documents/카카오톡 받은 파일/휴인미 game result 복사본 (1).xlsx"
data = pd.ExcelFile(file_path)

# Load the first sheet
df = data.parse(data.sheet_names[0])

# Display the first few rows to understand the structure
print(df.head())

# Group the data by member_id
grouped = df.groupby('member_id')

# 특정 member_id를 지정 (None이면 모든 멤버 출력)
target_member_id = 2  # 원하는 member_id를 입력 (None으로 설정하면 모든 멤버 처리)


# Visualize for each member
for member_id, group in grouped:

    # 특정 member_id가 설정된 경우, 해당 멤버만 처리
    if target_member_id is not None and member_id != target_member_id:
        continue

    for _, row in group.iterrows():
        user_answer = row['user_answer']
        card_type = row['card_type']
        card_count = row['card_count']
        plot_user_answer_grid(member_id, user_answer, card_type, card_count)
