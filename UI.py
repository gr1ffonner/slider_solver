import tkinter
from main import solve_captcha

# Создание окна
window = tkinter.Tk()
window.title("Решение капчи")

# Создание кнопки "Решить"
solve_button = tkinter.Button(window, text="Решить", command=solve_captcha)
solve_button.pack(pady=10)

# Запуск главного цикла обработки событий
window.mainloop()