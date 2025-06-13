# Packages
from customtkinter import *
from PIL import Image
from io import BytesIO

# History
from utils import history

# Models initialization
from models.deepseek import query_deepseek
from models.anthropic import query_anthropic
from models.gryphe import query_gryphe
from models.llama3 import query_llama3
from models.mistralai import query_mistralai
from models.flux import query_flux

# Utils
from utils.event_handlers import on_entry_change

# Constants
from config.constants import LIGHT_THEME, DARK_THEME

# Global variables
model_name = ""

# Flags
create_frame = True
scroll_bar_frame_created = False
fist_time_created = True
auto_save_images_flag = False
display_logs_flag = False
theme_flag = 1
language_flag = 1


# Functions


def open_settings():
    global auto_save_images_var, display_logs_var, auto_save_images_flag, display_logs_flag, theme_flag, language_flag

    settings_window = CTkToplevel(root)
    settings_window.title("Settings")
    settings_window.geometry()
    settings_window.geometry("500x400")
    settings_window.resizable("False", "False")
    settings_window.attributes("-topmost", True)

    # Interface
    settings_label = CTkLabel(
        settings_window,
        text="Settings",
        fg_color="transparent",
        text_color="black",
        font=("Arial", 20, "bold"),
    )
    settings_label.place(relx=0.15, rely=0.1, anchor="center")

    # General settings
    theme_settings_label = CTkLabel(
        settings_window,
        text="Theme:",
        fg_color="transparent",
        text_color="black",
        font=("Arial", 15),
    )
    theme_settings_label.place(relx=0.125, rely=0.2, anchor="center")

    if theme_flag == 1:
        theme_var = IntVar(value=1)
    else:
        theme_var = IntVar(value=2)

    def change_theme():
        theme = theme_var.get()
        if theme == 1:
            root._set_appearance_mode("light")
            dialogue_entry.configure(
                fg_color=LIGHT_THEME["entry_fg"], text_color=LIGHT_THEME["entry_text"]
            )
            if scroll_bar_frame_created:
                scroll_bar_frame.configure(fg_color=LIGHT_THEME["bg"])
        else:
            root._set_appearance_mode("dark")
            welcome_phrase.configure(text_color="black")
            dialogue_entry.configure(
                fg_color=DARK_THEME["entry_fg"], text_color=DARK_THEME["entry_text"]
            )
            if scroll_bar_frame_created:
                scroll_bar_frame.configure(fg_color=DARK_THEME["bg"])

    light_theme_btn = CTkRadioButton(
        settings_window,
        text="Light",
        variable=theme_var,
        value=1,
        border_color="gray",
        hover_color="black",
        fg_color="black",
        command=change_theme,
    )
    light_theme_btn.place(relx=0.3, rely=0.2, anchor="center")

    dark_theme_btn = CTkRadioButton(
        settings_window,
        text="Dark",
        variable=theme_var,
        value=2,
        border_color="gray",
        hover_color="black",
        fg_color="black",
        command=change_theme,
    )
    dark_theme_btn.place(relx=0.45, rely=0.2, anchor="center")

    # Checkbox buttons
    # 1
    if auto_save_images_flag:
        auto_save_images_var = StringVar(value="on")
    else:
        auto_save_images_var = StringVar(value="off")

    auto_save_images_checkbox = CTkCheckBox(
        settings_window,
        text="Auto save images",
        variable=auto_save_images_var,
        fg_color="black",
        hover_color="black",
        checkmark_color="white",
        onvalue="on",
        offvalue="off",
    )
    auto_save_images_checkbox.place(relx=0.2, rely=0.3, anchor="center")

    # 2
    if display_logs_flag:
        display_logs_var = StringVar(value="on")
    else:
        display_logs_var = StringVar(value="off")

    display_logs_checkbox = CTkCheckBox(
        settings_window,
        text="Display logs in the console",
        variable=display_logs_var,
        fg_color="black",
        hover_color="black",
        checkmark_color="white",
        onvalue="on",
        offvalue="off",
    )
    display_logs_checkbox.place(relx=0.25, rely=0.4, anchor="center")

    # Language
    language_settings_label = CTkLabel(
        settings_window,
        text="Language:",
        fg_color="transparent",
        text_color="black",
        font=("Arial", 15),
    )
    language_settings_label.place(relx=0.145, rely=0.5, anchor="center")

    def language_function(choice):
        print("optionmenu dropdown clicked:", choice)
        if choice == "Ukrainian":
            choose_your_ai_label.configure(text="Чат-боти")
            image_generation_ai_label.configure(text="Генерація зображень")
            welcome_phrase.configure(text="Ви побачите відповідь моделі тут")
            send_btn.configure(text="Надіслати")
        elif choice == "English":
            choose_your_ai_label.configure(text="Chat bots")
            image_generation_ai_label.configure(text="Image generation")
            welcome_phrase.configure(text="You’ll see the model’s answer here")
            send_btn.configure(text="Send")

    if language_flag == 1:
        language_var = StringVar(value="English")
    else:
        language_var = StringVar(value="Ukrainian")

    language_menu = CTkOptionMenu(
        settings_window,
        values=["English", "Ukrainian"],
        command=language_function,
        variable=language_var,
        fg_color="white",
        dropdown_fg_color="white",
        button_color="white",
        button_hover_color="gray",
        text_color="black",
        corner_radius=10,
    )
    language_menu.place(relx=0.375, rely=0.5, anchor="center")

    # Settings buttons
    def save_settings():
        global auto_save_images_flag, display_logs_flag, theme_flag, language_flag
        if auto_save_images_var.get() == "on":
            auto_save_images_flag = True
        else:
            auto_save_images_flag = False

        if display_logs_var.get() == "on":
            display_logs_flag = True
        else:
            display_logs_flag = False

        if theme_var.get() == 1:
            theme_flag = 1
        else:
            theme_flag = 2

        if language_var.get() == "English":
            language_flag = 1
        else:
            language_flag = 2

        settings_window.destroy()

    save_settings_btn = CTkButton(
        master=settings_window,
        text="Save",
        width=100,
        height=50,
        fg_color=DARK_THEME["entry_fg"],
        hover_color="#44494D",
        text_color="white",
        font=("Segoe UI", 15),
        command=save_settings,
    )
    save_settings_btn.place(relx=0.6, rely=0.875, anchor="center")

    def cancel_settings():
        global theme_var, theme_flag, auto_save_images_flag, display_logs_flag, language_flag, language_var, auto_save_images_var, display_logs_var
        settings_window.destroy()

        # Theme
        theme_var = IntVar(value=1)
        theme_flag = 1
        dialogue_entry.configure(
            fg_color=LIGHT_THEME["entry_fg"], text_color=LIGHT_THEME["entry_text"]
        )
        root._set_appearance_mode("light")

        # Auto save
        auto_save_images_flag = False
        auto_save_images_var = StringVar(value="off")

        # Auto save
        display_logs_flag = False
        display_logs_var = StringVar(value="off")

        # Language
        language_flag = 1
        language_var = StringVar(value="English")
        choose_your_ai_label.configure(text="Chat bots")
        image_generation_ai_label.configure(text="Image generation")
        welcome_phrase.configure(text="You’ll see the model’s answer here")
        send_btn.configure(text="Send")

        # Scroll bar frame
        scroll_bar_frame.configure(fg_color=LIGHT_THEME["bg"])

    settings_window.protocol("WM_DELETE_WINDOW", cancel_settings)

    cancel_settings_btn = CTkButton(
        master=settings_window,
        text="Cancel",
        width=100,
        height=50,
        fg_color="white",
        text_color="black",
        hover_color="#dbdbdb",
        font=("Segoe UI", 15),
        command=cancel_settings,
    )
    cancel_settings_btn.place(relx=0.85, rely=0.875, anchor="center")


def create_scrollable_frame():
    global scroll_bar_frame, scroll_bar_frame_created

    if theme_flag == 1:
        scroll_bar_frame = CTkScrollableFrame(
            master=dialogue_window,
            width=685,
            height=500,
            border_width=2,
            corner_radius=0,
            fg_color=LIGHT_THEME["bg"],
        )
    else:
        scroll_bar_frame = CTkScrollableFrame(
            master=dialogue_window,
            width=685,
            height=500,
            border_width=2,
            corner_radius=0,
            fg_color=DARK_THEME["bg"],
        )

    scroll_bar_frame.place(relx=0.5, rely=0.5, anchor="center")
    scroll_bar_frame_created = True


def open_dialogue_window(model):
    global send_btn, model_name, dialogue_entry, scroll_bar_frame, create_frame, scroll_bar_frame_created, fist_time_created, welcome_phrase

    # Delete prev items
    if scroll_bar_frame_created:
        scroll_bar_frame.destroy()
        scroll_bar_frame_created = False
        create_frame = True

    try:
        dialogue_entry.destroy()
    except:
        pass

    try:
        select_model_label.destroy()
    except:
        pass

    # Settings
    settings_frame = CTkFrame(
        master=dialogue_window, width=700, height=100, fg_color="white"
    )
    settings_frame.place(relx=0.5, rely=0, anchor="n")

    settings_img = CTkImage(Image.open("./images/settings_btn.webp"), size=(50, 50))

    settings_btn = CTkButton(
        master=settings_frame,
        width=50,
        height=50,
        image=settings_img,
        fg_color="transparent",
        hover_color="#dedede",
        text="",
        command=open_settings,
    )
    settings_btn.place(relx=0.9, rely=0.5, anchor="center")

    # Model name
    model_name_top_label = CTkLabel(
        master=settings_frame,
        text=f"{model_name}",
        text_color="black",
        font=("Segoe UI", 20),
    )
    model_name_top_label.place(relx=0.2, rely=0.5, anchor="center")

    # Model img
    model_logo_img = CTkImage(Image.open("./images/profile.jpg"), size=(50, 50))

    if model == "gryphe":
        model_logo_img = CTkImage(
            Image.open("./images/models/gryphe.webp"), size=(50, 50)
        )
        model_name_top_label.place(relx=0.19, rely=0.5, anchor="center")

    elif model == "deepseek_v3":
        model_logo_img = CTkImage(
            Image.open("./images/models/deepseek.webp"), size=(50, 50)
        )
        model_name_top_label.place(relx=0.235, rely=0.5, anchor="center")

    elif model == "flux":
        model_logo_img = CTkImage(
            Image.open("./images/models/flux.webp"), size=(50, 50)
        )
        model_name_top_label.place(relx=0.19, rely=0.5, anchor="center")

    elif model == "Llama3":
        model_logo_img = CTkImage(
            Image.open("./images/models/llama3.webp"), size=(50, 50)
        )

    elif model == "mistralai":
        model_logo_img = CTkImage(
            Image.open("./images/models/mistralai.png"), size=(50, 50)
        )
        model_name_top_label.place(relx=0.23, rely=0.5, anchor="center")

    elif model == "anthropic":
        model_logo_img = CTkImage(
            Image.open("./images/models/anthropic.png"), size=(50, 50)
        )
        model_name_top_label.place(relx=0.23, rely=0.5, anchor="center")

    model_logo_img_label = CTkLabel(
        master=settings_frame, fg_color="transparent", image=model_logo_img, text=""
    )
    model_logo_img_label.place(relx=0.1, rely=0.5, anchor="center")

    # Entry
    entry_frame = CTkFrame(
        master=dialogue_window, width=700, height=100, fg_color="white"
    )
    entry_frame.place(relx=0.5, rely=1.0, anchor="s")

    entry_variable = StringVar()
    entry_variable.trace_add(
        "write", lambda *args: on_entry_change(dialogue_entry, send_btn, *args)
    )

    if theme_flag == 1:
        dialogue_entry_fg = DARK_THEME["entry_text"]
        dialogue_entry_text = "#000"
    else:
        dialogue_entry_fg = DARK_THEME["entry_fg"]
        dialogue_entry_text = DARK_THEME["entry_text"]

    dialogue_entry = CTkEntry(
        master=entry_frame,
        width=500,
        height=50,
        font=("Segoe UI", 15),
        corner_radius=5,
        justify="left",
        textvariable=entry_variable,
        fg_color=f"{dialogue_entry_fg}",
        text_color=f"{dialogue_entry_text}",
    )
    dialogue_entry.place(relx=0.4, rely=0.5, anchor="center")

    if language_flag == 2:
        send_btn_text = "Надіслати"
    else:
        send_btn_text = "Send"

    send_btn = CTkButton(
        master=entry_frame,
        text=send_btn_text,
        width=100,
        height=50,
        fg_color=DARK_THEME["entry_fg"],
        text_color="white",
        hover_color="#44494D",
        font=("Segoe UI", 15),
        state="disabled",
    )
    send_btn.place(relx=0.85, rely=0.5, anchor="center")

    # Welcome phrase
    if fist_time_created:
        if language_flag == 2:
            message = "Ви побачите відповідь моделі тут"
        else:
            message = "You’ll see the model’s answer here"

        welcome_phrase = CTkLabel(
            master=dialogue_window,
            text=message,
            font=("Segoe UI", 25),
            fg_color="transparent",
        )
        welcome_phrase.place(relx=0.5, rely=0.4, anchor="center")

    # Call model func
    if model == "deepseek_v3":
        model_name = "Deepseek V3"
        # Buttons
        deepseek_btn.configure(state="disabled")
        anthropic_btn.configure(state="normal")
        gryphe_btn.configure(state="normal")
        flux_btn.configure(state="normal")
        Llama3_btn.configure(state="normal")
        mistralai_btn.configure(state="normal")

        dialogue_entry.bind("<Return>", deepseekV3)
        send_btn.configure(command=deepseekV3)

        if history.MODELS_HISTORY["deepseek"]["questions"]:
            deepseekV3()
            for question, answer in zip(
                history.MODELS_HISTORY["deepseek"]["questions"],
                history.MODELS_HISTORY["deepseek"]["answers"],
            ):
                print("Question:", question)
                question_label = CTkLabel(
                    scroll_bar_frame,
                    text=f"{question}",
                    wraplength=200,
                    fg_color="white",
                    padx=5,
                    pady=5,
                    corner_radius=5,
                )
                question_label.pack(anchor="e", padx=15, pady=10)

                print("Answer:", answer)
                answer_label = CTkLabel(
                    master=scroll_bar_frame,
                    text=f"{answer}",
                    wraplength=400,
                    fg_color="white",
                    padx=5,
                    pady=5,
                    corner_radius=5,
                )
                answer_label.pack(anchor="w", padx=15, pady=10)

    elif model == "flux":
        model_name = "Flux"
        # Buttons
        flux_btn.configure(state="disabled")
        anthropic_btn.configure(state="normal")
        gryphe_btn.configure(state="normal")
        deepseek_btn.configure(state="normal")
        Llama3_btn.configure(state="normal")
        mistralai_btn.configure(state="normal")

        dialogue_entry.bind("<Return>", flux)
        send_btn.configure(command=flux)
        if history.MODELS_HISTORY["flux"]["questions"]:
            flux()
            for question, image in zip(
                history.MODELS_HISTORY["flux"]["questions"],
                history.MODELS_HISTORY["flux"]["answers"],
            ):
                print("Question:", question)
                question_label = CTkLabel(
                    scroll_bar_frame,
                    text=f"{question}",
                    wraplength=200,
                    fg_color="white",
                    padx=5,
                    pady=5,
                    corner_radius=5,
                )
                question_label.pack(anchor="e", padx=15, pady=10)

                img_data = BytesIO(image.content)
                img = CTkImage(Image.open(img_data), size=(650, 400))
                img_label = CTkLabel(
                    master=scroll_bar_frame,
                    text="",
                    wraplength=650,
                    fg_color="white",
                    image=img,
                )
                img_label.pack(anchor="w", padx=10, pady=5)

                # =====================
                def save_image():
                    file_path = filedialog.asksaveasfilename(
                        defaultextension=".png",
                        filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                        title="Save image as",
                    )

                    if file_path:
                        img_to_save = Image.open(img_data)
                        img_to_save.save(file_path)

                # =====================

                save_img = CTkImage(
                    Image.open("./images/download_icon.jpg"), size=(25, 25)
                )
                save_img_btn = CTkButton(
                    img_label,
                    text="",
                    width=25,
                    height=25,
                    fg_color="transparent",
                    hover_color="#d4d4d4",
                    image=save_img,
                    border_width=2,
                    border_color="black",
                    command=save_image,
                )
                save_img_btn.place(x=600, y=10)

    elif model == "gryphe":
        model_name = "Gryphe"
        # Buttons
        gryphe_btn.configure(state="disabled")
        anthropic_btn.configure(state="normal")
        flux_btn.configure(state="normal")
        deepseek_btn.configure(state="normal")
        Llama3_btn.configure(state="normal")
        mistralai_btn.configure(state="normal")

        dialogue_entry.bind("<Return>", gryphe)
        send_btn.configure(command=gryphe)

        if history.MODELS_HISTORY["gryphe"]["questions"]:
            gryphe()
            for question, answer in zip(
                history.MODELS_HISTORY["gryphe"]["questions"],
                history.MODELS_HISTORY["gryphe"]["answers"],
            ):
                print("Question:", question)
                question_label = CTkLabel(
                    scroll_bar_frame,
                    text=f"{question}",
                    wraplength=200,
                    fg_color="white",
                    padx=5,
                    pady=5,
                    corner_radius=5,
                )
                question_label.pack(anchor="e", padx=15, pady=10)

                print("Answer:", answer)
                answer_label = CTkLabel(
                    master=scroll_bar_frame,
                    text=f"{answer}",
                    wraplength=400,
                    fg_color="white",
                    padx=5,
                    pady=5,
                    corner_radius=5,
                )
                answer_label.pack(anchor="w", padx=15, pady=10)

    elif model == "Llama3":
        model_name = "Llama3"

        # Buttons
        Llama3_btn.configure(state="disabled")
        anthropic_btn.configure(state="normal")
        gryphe_btn.configure(state="normal")
        flux_btn.configure(state="normal")
        deepseek_btn.configure(state="normal")
        mistralai_btn.configure(state="normal")

        dialogue_entry.bind("<Return>", Llama3)
        send_btn.configure(command=Llama3)

        if history.MODELS_HISTORY["llama3"]["questions"]:
            Llama3()
            for question, answer in zip(
                history.MODELS_HISTORY["llama3"]["questions"],
                history.MODELS_HISTORY["llama3"]["answers"],
            ):
                print("Question:", question)
                question_label = CTkLabel(
                    scroll_bar_frame,
                    text=f"{question}",
                    wraplength=200,
                    fg_color="white",
                    padx=5,
                    pady=5,
                    corner_radius=5,
                )
                question_label.pack(anchor="e", padx=15, pady=10)

                print("Answer:", answer)
                answer_label = CTkLabel(
                    master=scroll_bar_frame,
                    text=f"{answer}",
                    wraplength=400,
                    fg_color="white",
                    padx=5,
                    pady=5,
                    corner_radius=5,
                )
                answer_label.pack(anchor="w", padx=15, pady=10)

    elif model == "mistralai":
        model_name = "Mistral AI"

        # Buttons
        mistralai_btn.configure(state="disabled")
        anthropic_btn.configure(state="normal")
        Llama3_btn.configure(state="normal")
        gryphe_btn.configure(state="normal")
        flux_btn.configure(state="normal")
        deepseek_btn.configure(state="normal")

        dialogue_entry.bind("<Return>", mistralai)
        send_btn.configure(command=mistralai)

        if history.MODELS_HISTORY["mistralai"]["questions"]:
            mistralai()
            for question, answer in zip(
                history.MODELS_HISTORY["mistralai"]["questions"],
                history.MODELS_HISTORY["mistralai"]["answers"],
            ):
                print("Question:", question)
                question_label = CTkLabel(
                    scroll_bar_frame,
                    text=f"{question}",
                    wraplength=200,
                    fg_color="white",
                    padx=5,
                    pady=5,
                    corner_radius=5,
                )
                question_label.pack(anchor="e", padx=15, pady=10)

                print("Answer:", answer)
                answer_label = CTkLabel(
                    master=scroll_bar_frame,
                    text=f"{answer}",
                    wraplength=400,
                    fg_color="white",
                    padx=5,
                    pady=5,
                    corner_radius=5,
                )
                answer_label.pack(anchor="w", padx=15, pady=10)

    elif model == "anthropic":
        model_name = "Anthropic"

        # Buttons
        anthropic_btn.configure(state="disabled")
        mistralai_btn.configure(state="normal")
        Llama3_btn.configure(state="normal")
        gryphe_btn.configure(state="normal")
        flux_btn.configure(state="normal")
        deepseek_btn.configure(state="normal")

        dialogue_entry.bind("<Return>", anthropic)
        send_btn.configure(command=anthropic)

        if history.MODELS_HISTORY["anthropic"]["questions"]:
            anthropic()
            for question, answer in zip(
                history.MODELS_HISTORY["anthropic"]["questions"],
                history.MODELS_HISTORY["anthropic"]["answers"],
            ):
                print("Question:", question)
                question_label = CTkLabel(
                    scroll_bar_frame,
                    text=f"{question}",
                    wraplength=200,
                    fg_color="white",
                    padx=5,
                    pady=5,
                    corner_radius=5,
                )
                question_label.pack(anchor="e", padx=15, pady=10)

                print("Answer:", answer)
                answer_label = CTkLabel(
                    master=scroll_bar_frame,
                    text=f"{answer}",
                    wraplength=400,
                    fg_color="white",
                    padx=5,
                    pady=5,
                    corner_radius=5,
                )
                answer_label.pack(anchor="w", padx=15, pady=10)

    model_name_label.configure(text=f"{model_name}")
    model_name_top_label.configure(text=f"{model_name}")


# Models
def deepseekV3(event=None):
    global create_frame, fist_time_created, question_label, answer_label
    if create_frame:
        create_scrollable_frame()
        create_frame = False
    fist_time_created = False

    user_question = dialogue_entry.get()

    if len(user_question) <= 0:
        return

    answer = query_deepseek(user_question)

    if display_logs_flag:
        print(answer)

    question_label = CTkLabel(
        scroll_bar_frame,
        text=f"{user_question}",
        wraplength=200,
        fg_color="white",
        padx=5,
        pady=5,
        corner_radius=5,
    )
    question_label.pack(anchor="e", padx=15, pady=10)

    # Width of the question_label
    root.update_idletasks()
    question_label_width = question_label.winfo_width()

    # Width of the answer_label
    answer_label_width = 650 - question_label_width

    answer_label = CTkLabel(
        master=scroll_bar_frame,
        text=f"{answer}",
        wraplength=answer_label_width,
        fg_color="white",
        padx=5,
        pady=5,
        corner_radius=5,
        # width=answer_label_width,
    )
    answer_label.pack(anchor="w", padx=15, pady=10)
    dialogue_entry.delete(0, END)


def flux(event=None):
    global create_frame, img_label, fist_time_created
    if create_frame:
        create_scrollable_frame()
        create_frame = False

    fist_time_created = False

    img_prompt = dialogue_entry.get()

    if len(img_prompt) <= 0:
        return

    image_data = query_flux(img_prompt)
    img = CTkImage(Image.open(image_data), size=(650, 400))

    if display_logs_flag:
        print(image_data)

    img_prompt_label = CTkLabel(
        scroll_bar_frame,
        text=f"{img_prompt}",
        fg_color="white",
        padx=5,
        pady=5,
        corner_radius=5,
    )
    img_prompt_label.pack(anchor="e", padx=25, pady=10)

    def save_image():
        if auto_save_images_flag:
            img_to_save = Image.open(image_data)
            img_to_save.save(f"images-from-ai/{img_prompt}.png")

            def close_info_window():
                info_window.destroy()

            if language_flag == 1:
                directory_text = (
                    "Your image has been saved to the folder\n'images-from-ai'"
                )
                close_btn_text = "Close"
            elif language_flag == 2:
                directory_text = "Ваше зображення збережено в папку\n'images-from-ai'"
                close_btn_text = "Закрити"

            info_window = CTkToplevel(root)
            info_window.title("Image directory")
            info_window.geometry("300x200")
            info_window.resizable("False", "False")
            info_window.attributes("-topmost", True)
            directory_info_label = CTkLabel(
                info_window,
                text=f"{directory_text}",
                width=40,
                height=28,
                fg_color="transparent",
            )
            directory_info_label.place(relx=0.5, rely=0.4, anchor="center")

            close_info_window_btn = CTkButton(
                info_window,
                text=f"{close_btn_text}",
                command=close_info_window,
            )
            close_info_window_btn.place(relx=0.5, rely=0.8, anchor="center")
        else:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                title="Save image as",
            )

            if file_path:
                img_to_save = Image.open(image_data)
                img_to_save.save(file_path)

    try:
        img_label = CTkLabel(
            master=scroll_bar_frame,
            text="",
            wraplength=650,
            fg_color="white",
            image=img,
        )
        if auto_save_images_flag:
            save_image()
        else:
            save_img = CTkImage(Image.open("./images/download_icon.jpg"), size=(25, 25))
            save_img_btn = CTkButton(
                img_label,
                text="",
                width=25,
                height=25,
                fg_color="transparent",
                hover_color="#d4d4d4",
                image=save_img,
                border_width=2,
                border_color="black",
                command=save_image,
            )
            save_img_btn.place(x=600, y=10)

    except:
        if not image_data:
            img_label = CTkLabel(
                master=scroll_bar_frame,
                text="An error occurred, try again later...",
                wraplength=650,
                fg_color="white",
                padx=5,
                pady=5,
                corner_radius=5,
            )

    img_label.pack(anchor="w", padx=10, pady=5)
    dialogue_entry.delete(0, END)


def gryphe(event=None):
    global create_frame, fist_time_created, question_label, answer_label
    if create_frame:
        create_scrollable_frame()
        create_frame = False
    fist_time_created = False

    user_question = dialogue_entry.get()

    if len(user_question) <= 0:
        return

    answer = query_gryphe(user_question)

    if display_logs_flag:
        print(answer)

    question_label = CTkLabel(
        scroll_bar_frame,
        text=f"{user_question}",
        wraplength=200,
        fg_color="white",
        padx=5,
        pady=5,
        corner_radius=5,
    )
    question_label.pack(anchor="e", padx=15, pady=10)

    # Width of the question_label
    root.update_idletasks()
    question_label_width = question_label.winfo_width()

    # Width of the answer_label
    answer_label_width = 650 - question_label_width

    answer_label = CTkLabel(
        master=scroll_bar_frame,
        text=f"{answer}",
        wraplength=answer_label_width,
        fg_color="white",
        padx=5,
        pady=5,
        corner_radius=5,
        # width=answer_label_width,
    )
    answer_label.pack(anchor="w", padx=15, pady=10)
    dialogue_entry.delete(0, END)


def Llama3(event=None):
    global create_frame, fist_time_created, question_label, answer_label
    if create_frame:
        create_scrollable_frame()
        create_frame = False
    fist_time_created = False

    user_question = dialogue_entry.get()

    if len(user_question) <= 0:
        return

    answer = query_llama3(user_question)

    if display_logs_flag:
        print(answer)

    question_label = CTkLabel(
        scroll_bar_frame,
        text=f"{user_question}",
        wraplength=200,
        fg_color="white",
        padx=5,
        pady=5,
        corner_radius=5,
    )
    question_label.pack(anchor="e", padx=15, pady=10)

    # Width of the question_label
    root.update_idletasks()
    question_label_width = question_label.winfo_width()

    # Width of the answer_label
    answer_label_width = 650 - question_label_width

    answer_label = CTkLabel(
        master=scroll_bar_frame,
        text=f"{answer}",
        wraplength=answer_label_width,
        fg_color="white",
        padx=5,
        pady=5,
        corner_radius=5,
        # width=answer_label_width,
    )
    answer_label.pack(anchor="w", padx=15, pady=10)
    dialogue_entry.delete(0, END)


def mistralai(event=None):
    global create_frame, fist_time_created, question_label, answer_label
    if create_frame:
        create_scrollable_frame()
        create_frame = False
    fist_time_created = False

    user_question = dialogue_entry.get()

    if len(user_question) <= 0:
        return

    answer = query_mistralai(user_question)

    if display_logs_flag:
        print(answer)

    question_label = CTkLabel(
        scroll_bar_frame,
        text=f"{user_question}",
        wraplength=200,
        fg_color="white",
        padx=5,
        pady=5,
        corner_radius=5,
    )
    question_label.pack(anchor="e", padx=15, pady=10)

    # Width of the question_label
    root.update_idletasks()
    question_label_width = question_label.winfo_width()

    # Width of the answer_label
    answer_label_width = 650 - question_label_width

    answer_label = CTkLabel(
        master=scroll_bar_frame,
        text=f"{answer}",
        wraplength=answer_label_width,
        fg_color="white",
        padx=5,
        pady=5,
        corner_radius=5,
        # width=answer_label_width,
    )
    answer_label.pack(anchor="w", padx=15, pady=10)
    dialogue_entry.delete(0, END)


def anthropic(event=None):
    global create_frame, fist_time_created, question_label, answer_label
    if create_frame:
        create_scrollable_frame()
        create_frame = False
    fist_time_created = False

    user_question = dialogue_entry.get()

    if len(user_question) <= 0:
        return

    answer = query_anthropic(user_question)

    if display_logs_flag:
        print(answer)

    question_label = CTkLabel(
        scroll_bar_frame,
        text=f"{user_question}",
        wraplength=200,
        fg_color="white",
        padx=5,
        pady=5,
        corner_radius=5,
    )
    question_label.pack(anchor="e", padx=15, pady=10)

    # Width of the question_label
    root.update_idletasks()
    question_label_width = question_label.winfo_width()

    # Width of the answer_label
    answer_label_width = 650 - question_label_width

    answer_label = CTkLabel(
        master=scroll_bar_frame,
        text=f"{answer}",
        wraplength=answer_label_width,
        fg_color="white",
        padx=5,
        pady=5,
        corner_radius=5,
        # width=answer_label_width,
    )
    answer_label.pack(anchor="w", padx=15, pady=10)
    dialogue_entry.delete(0, END)


# Window
root = CTk()
root.geometry("1000x700")
root.minsize(1000, 700)
root.title("LLM & Gen")
root.iconbitmap("./images/app-logo.ico")
root.resizable("False", "False")
set_appearance_mode("light")


# Buttons frame
buttons_frame = CTkFrame(
    master=root, width=300, fg_color=DARK_THEME["entry_fg"], corner_radius=0
)
buttons_frame.pack(fill="y", side="left")

# Labels
model_name_label = CTkLabel(
    master=buttons_frame,
    text=f"{model_name}",
    text_color="white",
    font=("Segoe UI", 20),
)
model_name_label.place(x=30, y=30)

choose_your_ai_label = CTkLabel(
    master=buttons_frame,
    text="Chat bots",
    text_color="white",
    font=("Segoe UI", 20),
)
choose_your_ai_label.place(x=30, y=100)

image_generation_ai_label = CTkLabel(
    master=buttons_frame,
    text="Image generation",
    text_color="white",
    font=("Segoe UI", 20),
)
image_generation_ai_label.place(x=30, y=450)

# Models buttons

# =============== Free models ===============
# 1
deepseek_btn = CTkButton(
    master=buttons_frame,
    text=f"deepseek-v3",
    width=250,
    height=40,
    anchor="center",
    font=("Segoe UI", 20),
    corner_radius=10,
    fg_color="#44494D",
    hover_color="#333333",
    command=lambda: open_dialogue_window("deepseek_v3"),
)
deepseek_btn.place(x=25, y=150)

# 2
gryphe_btn = CTkButton(
    master=buttons_frame,
    text="gryphe",
    width=250,
    height=40,
    anchor="center",
    font=("Segoe UI", 20),
    corner_radius=10,
    fg_color="#44494D",
    hover_color="#333333",
    command=lambda: open_dialogue_window("gryphe"),
)
gryphe_btn.place(x=25, y=200)

# 3
mistralai_btn = CTkButton(
    master=buttons_frame,
    text="mistral-ai",
    width=250,
    height=40,
    anchor="center",
    font=("Segoe UI", 20),
    corner_radius=10,
    fg_color="#44494D",
    hover_color="#333333",
    command=lambda: open_dialogue_window("mistralai"),
)
mistralai_btn.place(x=25, y=250)

# 4
anthropic_btn = CTkButton(
    master=buttons_frame,
    text="anthropic-ai",
    width=250,
    height=40,
    anchor="center",
    font=("Segoe UI", 20),
    corner_radius=10,
    fg_color="#44494D",
    hover_color="#333333",
    command=lambda: open_dialogue_window("anthropic"),
)
anthropic_btn.place(x=25, y=300)

# 5
Llama3_btn = CTkButton(
    master=buttons_frame,
    text="llama3",
    width=250,
    height=40,
    anchor="center",
    font=("Segoe UI", 20),
    corner_radius=10,
    fg_color="#44494D",
    hover_color="#333333",
    command=lambda: open_dialogue_window("Llama3"),
)
Llama3_btn.place(x=25, y=350)

# =============== Image generation models ===============
# 1
flux_btn = CTkButton(
    master=buttons_frame,
    text="flux",
    width=250,
    height=40,
    anchor="center",
    font=("Segoe UI", 20),
    corner_radius=10,
    fg_color="#44494D",
    hover_color="#333333",
    command=lambda: open_dialogue_window("flux"),
)
flux_btn.place(x=25, y=500)

# Dialogue Window
dialogue_window = CTkFrame(master=root, width=700, height=700, fg_color="white")
dialogue_window.pack(fill="y", side="left")

select_model_label = CTkLabel(
    master=dialogue_window,
    text="Select a model",
    font=("Segoe UI", 20),
    fg_color="transparent",
)
select_model_label.place(relx=0.5, rely=0.5, anchor="center")

root.mainloop()
