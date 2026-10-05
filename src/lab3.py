"""
Лабораторна робота № 3: Операції зі структурами даних
Варіант 13: Аналіз медичних даних (пацієнти, діагнози, лікування)
"""

from collections import defaultdict
from functools import reduce

# 1. Початковий набір даних (список словників)
patients_data = [
    {
        "id": 1,
        "name": "Тадеуш Ковальский",
        "age": 45,
        "diagnosis": "Гіпертонія",
        "cost": 1200.50,
        "medications": {"Lisinopril", "Aspirin"}
    },
    {
        "id": 2,
        "name": "Адам Новак",
        "age": 32,
        "diagnosis": "Грип",
        "cost": 450.00,
        "medications": {"Paracetamol", "Ibuprofen", "Vitamin C"}
    },
    {
        "id": 3,
        "name": "Яцек Левандовський",
        "age": 60,
        "diagnosis": "Цукровий діабет",
        "cost": 3100.00,
        "medications": {"Metformin", "Aspirin"}
    },
    {
        "id": 4,
        "name": "Томаш Камінський",
        "age": 28,
        "diagnosis": "Грип",
        "cost": 500.00,
        "medications": {"Paracetamol", "Amoxicillin"}
    },
    {
        "id": 5,
        "name": "Марек Потоцький",
        "age": 52,
        "diagnosis": "Гіпертонія",
        "cost": 1850.00,
        "medications": {"Amlodipine", "Lisinopril"}
    }
]


# 2. Базові операції зі структурами даних (CRUD)
def add_patient(data, patient):
    """Додає нового пацієнта."""
    data.append(patient)
    print("Запис про пацієнта успішно додано.")

def remove_patient(data, patient_id):
    """Видаляє пацієнта за унікальним ID."""
    initial_len = len(data)
    data[:] = [p for p in data if p["id"] != patient_id]
    if len(data) < initial_len:
        print(f"Пацієнта з ID {patient_id} успішно видалено.")
    else:
        print("Пацієнта з таким ID не знайдено.")

def update_patient(data, patient_id, key, value):
    """Оновлює дані пацієнта."""
    for p in data:
        if p["id"] == patient_id:
            if key in ["age", "id"]:
                value = int(value)
            elif key == "cost":
                value = float(value)
            elif key == "medications":
                # Перетворення рядка ліків через кому у множину (set)
                value = set(med.strip() for med in value.split(","))
            
            p[key] = value
            print("Дані пацієнта успішно оновлено.")
            return
    print("Пацієнта з таким ID не знайдено.")


# 3. Пошук та фільтрація (з використанням filter, map)
def find_by_diagnosis(data, diagnosis):
    """Шукає пацієнтів за діагнозом (використовує filter)."""
    return list(filter(lambda p: p["diagnosis"].lower() == diagnosis.lower(), data))

def get_patient_names_uppercase(data):
    """Повертає список імен пацієнтів у верхньому регістрі (використовує map)."""
    return list(map(lambda p: p["name"].upper(), data))


# 4. Аналітичні та статистичні функції (з використанням reduce)
def calculate_total_cost(data):
    """Обчислює загальну вартість лікування всіх пацієнтів (використовує reduce)."""
    return reduce(lambda acc, p: acc + p["cost"], data, 0.0)

def calculate_age_stats(data):
    """Обчислює середній, мінімальний та максимальний вік пацієнтів."""
    if not data:
        return 0, 0, 0
    ages = [p["age"] for p in data]
    avg_age = sum(ages) / len(ages)
    return avg_age, min(ages), max(ages)


# 5. Сортування та зрізи
def get_top_expensive_patients(data, top_n=3):
    """Сортує пацієнтів за вартістю лікування та повертає Top-N через зріз."""
    sorted_data = sorted(data, key=lambda p: p["cost"], reverse=True)
    return sorted_data[:top_n]


# 6. Робота з множинами та словниками
def group_patients_by_diagnosis(data):
    """Групує пацієнтів за діагнозами за допомогою defaultdict."""
    grouped = defaultdict(list)
    for p in data:
        grouped[p["diagnosis"]].append(p["name"])
    return dict(grouped)

def analyze_medications_sets(data):
    """Виконує операції з множинами ліків (унікальні та спільні)."""
    if not data:
        return set(), set()
    
    # Усі унікальні ліки (об'єднання множин)
    all_meds = set().union(*(p["medications"] for p in data))
    
    # Ліки, які призначені усім пацієнтам (перетин множин)
    common_meds = set.intersection(*(p["medications"] for p in data))
    
    return all_meds, common_meds


# 7. Інтерактивне меню
def print_menu():
    """Виводить меню програми."""
    print("\n==== СИСТЕМА АНАЛІЗУ МЕДИЧНИХ ДАНИХ ====")
    print("1. Показати всіх пацієнтів")
    print("2. Додати нового пацієнта")
    print("3. Видалити пацієнта за ID")
    print("4. Оновити дані пацієнта")
    print("5. Пошук пацієнтів за діагнозом (filter)")
    print("6. Загальна вартість лікування (reduce)")
    print("7. Статистика віку пацієнтів (сер/min/max)")
    print("8. Групування пацієнтів за діагнозом (словники)")
    print("9. Топ пацієнтів за вартістю лікування (сорт + зрізи)")
    print("10. Аналіз ліків (операції з множинами)")
    print("0. Вийти")

def main():
    global patients_data
    
    while True:
        print_menu()
        choice = input("Оберіть опцію (0-10): ").strip()

        if choice == "1":
            if not patients_data:
                print("База даних порожня.")
            else:
                for p in patients_data:
                    meds_str = ", ".join(p["medications"])
                    print(f"ID: {p['id']} | Ім'я: {p['name']} | Вік: {p['age']} | "
                          f"Діагноз: {p['diagnosis']} | Вартість лікування: {p['cost']:.2f} грн | Ліки: [{meds_str}]")

        elif choice == "2":
            try:
                p_id = int(input("Введіть ID: "))
                name = input("Введіть ПІБ пацієнта: ")
                age = int(input("Введіть вік: "))
                diagnosis = input("Введіть діагноз: ")
                cost = float(input("Введіть вартість лікування: "))
                meds_input = input("Введіть ліки через кому: ")
                medications = set(m.strip() for m in meds_input.split(",") if m.strip())

                new_p = {
                    "id": p_id, "name": name, "age": age,
                    "diagnosis": diagnosis, "cost": cost,
                    "medications": medications
                }
                add_patient(patients_data, new_p)
            except ValueError:
                print("Помилка! Введено некоректні числові дані.")

        elif choice == "3":
            try:
                p_id = int(input("Введіть ID пацієнта для видалення: "))
                remove_patient(patients_data, p_id)
            except ValueError:
                print("Помилка! ID має бути цілим числом.")

        elif choice == "4":
            try:
                p_id = int(input("Введіть ID пацієнта для оновлення: "))
                key = input("Введіть поле (name/age/diagnosis/cost/medications): ").strip()
                val = input("Введіть нове значення: ")
                update_patient(patients_data, p_id, key, val)
            except ValueError:
                print("Помилка введення даних.")

        elif choice == "5":
            diag = input("Введіть діагноз для пошуку: ")
            results = find_by_diagnosis(patients_data, diag)
            if results:
                print(f"Знайдено пацієнтів ({len(results)}):")
                for p in results:
                    print(f" - {p['name']} (Вік: {p['age']}, Вартість: {p['cost']})")
            else:
                print("Пацієнтів з таким діагнозом не знайдено.")

        elif choice == "6":
            total = calculate_total_cost(patients_data)
            print(f"Загальна вартість лікування всіх пацієнтів: {total:.2f} грн")

        elif choice == "7":
            avg_a, min_a, max_a = calculate_age_stats(patients_data)
            print(f"Вік пацієнтів: Середній = {avg_a:.1f} р. | Наймолодший = {min_a} р. | Найстарший = {max_a} р.")

        elif choice == "8":
            grouped = group_patients_by_diagnosis(patients_data)
            print("\nРозподіл пацієнтів за діагнозами:")
            for diag, names in grouped.items():
                print(f"  * {diag}: {', '.join(names)}")

        elif choice == "9":
            try:
                n = int(input("Скільки найдорожчих випадків вивести (наприклад, 3)? "))
                top_patients = get_top_expensive_patients(patients_data, n)
                print(f"\nТоп-{n} найдорожчих лікувань:")
                for p in top_patients:
                    print(f"  - {p['name']} ({p['diagnosis']}): {p['cost']:.2f} грн")
            except ValueError:
                print("Помилка! Введіть ціле число.")

        elif choice == "10":
            all_meds, common_meds = analyze_medications_sets(patients_data)
            print(f"Усі унікальні медикаменти у базі ({len(all_meds)}): {', '.join(all_meds)}")
            if common_meds:
                print(f"Спільні ліки для ВСІХ пацієнтів: {', '.join(common_meds)}")
            else:
                print("Спільних ліків для всіх пацієнтів немає.")

        elif choice == "0":
            print("Завершення роботи програми.")
            break

        else:
            print("Невірний вибір. Введіть число від 0 до 10.")

if __name__ == "__main__":
    main()
