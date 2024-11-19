# -*- coding: utf-8 -*-
"""
This program is a survey (questionnaire) containing questions from:

Programmer: Kopkrit SaiKeaw and Kitimapond Rattanadoung
Date: 2024.08.20
"""

from tkinter import (Tk, Label, ttk, Button, Radiobutton, Frame, Menu,
                     messagebox, StringVar, Listbox, BROWSE, END, Toplevel, Entry, IntVar,
                     TclError)
import time
import os.path
import datetime
import os
import csv

# create empty lists used for each set of questions
general_answers_list = []
MAA_list = []
FFMQ_SF_list = []
PHLMS_list = []
RuminativeThinking_list = []
NonAttachmentToSelf_list = []
PerceivedStress_list = []
OverallEmotionalWellbeing_list = []
current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
status = 'Pre_'

custom_font = ("Sarabun", 20)

def dialogBox(title, message):
    """
    Basic function to create and display general dialog boxes with a default font.
    """
    dialog = Tk()
    dialog.wm_title(title)
    dialog.grab_set()
    dialogWidth, dialogHeight = 600, 400
    positionRight = int(dialog.winfo_screenwidth() / 2 - dialogWidth / 2)
    positionDown = int(dialog.winfo_screenheight() / 2 - dialogHeight / 2)
    dialog.geometry(f"{dialogWidth}x{dialogHeight}+{positionRight}+{positionDown}")
    dialog.maxsize(dialogWidth, dialogHeight)

    # Apply 'Sarabun' font with size 20 for the label
    label = Label(dialog, text=message, font=custom_font)
    label.pack(side="top", fill="x", pady=10)

    # # Define a custom style for the button to use 'Sarabun' font, size 20
    # style = ttk.Style()
    # style.configure("Custom.TButton", font=custom_font, padding=6)  # padding to enhance size

    # Define a custom style for the button with 'Sarabun' font, size 20
    style = ttk.Style()
    style.configure("Sarabun.TButton", font=('Sarabun', 20))

    # Apply the custom style to the button
    ok_button = ttk.Button(dialog, text="ตกลง", style="Sarabun.TButton", command=dialog.destroy)
    ok_button.pack(ipady=3, pady=10)

    dialog.mainloop()


# Global variable to store the dialog instance
current_dialog = None

def nextSurveyDialog(title, message, cmd):
    """
    Dialog box that appears before moving onto the next set of questions with Sarabun font size 20,
    with extra space above and below the text.
    """
    global current_dialog

    # Close the previous dialog if it exists
    if current_dialog is not None and current_dialog.winfo_exists():
        current_dialog.destroy()

    # Create a new dialog
    current_dialog = Toplevel()
    current_dialog.title(title)
    current_dialog.grab_set()  # Make the dialog modal
    current_dialog.attributes('-fullscreen', True)

    # Create a style for Sarabun font
    s = ttk.Style()
    s.configure("Sarabun.TLabel", font=("Sarabun", 20))
    s.configure("Sarabun.TButton", font=("Sarabun", 20))

    # Add empty lines before text
    Label(current_dialog, text=" ", font=("Sarabun", 20)).pack(pady=20)
    Label(current_dialog, text=" ", font=("Sarabun", 20)).pack(pady=20)

    # Center the label text inside the dialog with additional spacing
    label = ttk.Label(current_dialog, text=message, style="Sarabun.TLabel", anchor='center', justify='center')
    label.pack(side="top", fill="both", pady=10, expand=True)

    # Add empty lines after text
    Label(current_dialog, text=" ", font=("Sarabun", 20)).pack(pady=20)
    Label(current_dialog, text=" ", font=("Sarabun", 20)).pack(pady=20)

    # OK button
    ok_button = ttk.Button(current_dialog, text="เริ่ม", style="Sarabun.TButton", command=lambda: [cmd(), current_dialog.destroy()])
    ok_button.pack(ipady=3, pady=10, expand=True, fill='x')

    # Prevent closing the dialog with the window close button
    current_dialog.protocol("WM_DELETE_WINDOW", disable_event)
    current_dialog.transient(current_dialog.master)  # Ensure it appears above the parent window

    current_dialog.mainloop()

def disable_event():
    pass


def finishedDialog(title, message):
    """
    Display the finished dialog box when the user reaches the end of the survey.
    """
    dialog = Tk()
    dialog.wm_title(title)
    dialog.grab_set()
    dialogWidth, dialogHeight = 600, 250  # Increased dimensions for a larger dialog
    positionRight = int(dialog.winfo_screenwidth() / 2 - dialogWidth / 2)
    positionDown = int(dialog.winfo_screenheight() / 2 - dialogHeight / 2)
    dialog.geometry("{}x{}+{}+{}".format(
        dialogWidth, dialogHeight, positionRight, positionDown))
    dialog.maxsize(dialogWidth, dialogHeight)
    dialog.overrideredirect(True)

    # Message label with Sarabun font size 20
    label = Label(dialog, text=message, font=("Sarabun", 20), wraplength=450, justify="center")
    label.pack(side="top", fill="x", pady=20)

    # OK button with larger font
    ok_button = ttk.Button(dialog, text="จบแบบสอบถาม", command=quit, style="Custom.TButton")
    ok_button.pack(ipady=10, pady=20)

    # Configure the style for the button
    s = ttk.Style()
    s.configure("Custom.TButton", font=("Sarabun", 20))

    # Prevent ALT + F4 from closing the dialog
    dialog.protocol("WM_DELETE_WINDOW", disable_event)
    dialog.mainloop()

class otherPopUpDialog(object):
    """
    Class for 'other' selections in General Question class.
    When user selects 'other' option, they are able to input
    their answer into an Entry widget.

    self.value: the value of Entry widget.
    """

    def __init__(self, master, text):
        top = self.top = Toplevel(master)
        self.text = text
        top.wm_title("Other Answers")
        top.grab_set()
        dialogWidth, dialogHeight = 200, 150
        positionRight = int(top.winfo_screenwidth() / 2 - dialogWidth / 2)
        positionDown = int(top.winfo_screenheight() / 2 - dialogHeight / 2)
        top.geometry("{}x{}+{}+{}".format(
            dialogWidth, dialogHeight, positionRight, positionDown))
        self.label = Label(top, text=self.text)
        self.label.pack(ipady=5)
        self.enter = Entry(top)
        self.enter.pack(ipady=5)
        self.ok_button = Button(top, text="ตกลง", command=self.cleanup)
        self.ok_button.pack(ipady=5)

    def cleanup(self):
        """
        Get input from Entry widget and close dialog.
        """
        self.value = self.enter.get()
        self.top.destroy()


class Survey(Tk):
    """
    Main class, define the container which will contain all the frames.
    """

    def __init__(self, *args, **kwargs):

        Tk.__init__(self, *args, **kwargs)

        # call closing protocol to create dialog box to ask
        # if user if they want to quit or not.
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        Tk.wm_title(self, "แบบประเมินสติ ความหมกมุ่นครุ่นคิด และสุขภาวะทางอารมณ์")

        # get position of window with respect to screen
        windowWidth, windowHeight = Tk.winfo_screenwidth(self), Tk.winfo_screenheight(self)
        positionRight = int(Tk.winfo_screenwidth(self) / 2 - windowWidth / 2)
        positionDown = int(Tk.winfo_screenheight(self) / 2 - windowHeight / 2)
        Tk.geometry(self, newGeometry="{}x{}+{}+{}".format(
            windowWidth, windowHeight, positionRight, positionDown))
        Tk.maxsize(self, windowWidth, windowHeight)

        # Create container Frame to hold all other classes,
        # which are the different parts of the survey.
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Create menu bar
        menubar = Menu(container)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Quit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        Tk.config(self, menu=menubar)

        # create empty dictionary for the different frames (the different classes)
        self.frames = {}

        for fr in (StartPage,
                   GenderQuestion,
                   AgeQuestion,
                   MindfulnessExperience,
                   MindfulnessExperienceDetail,
                   MindfulAttentionAwarenessScale,
                   FFMQ_SF,
                   PHLMS,
                   RuminativeThinkingScale,
                   NonAttachmentToSelf,
                   PerceivedStress,
                   OverallEmotionalWellbeing,
                   ):
            frame = fr(container, self)
            self.frames[fr] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def on_closing(self):
        """
        Display dialog box before quitting.
        """
        if messagebox.askokcancel("ออก", "คุณต้องการออกจากแบบสอบถาม?"):
            self.destroy()

    def show_frame(self, cont):
        """
        Used to display a frame.
        """
        frame = self.frames[cont]
        frame.tkraise()  # bring a frame to the "top"


class StartPage(Frame):
    """
    First page that user will see.
    Explains the rules and any extra information the user may need
    before beginning the survey.
    User can either click one of the two buttons, Begin Survey or Quit.
    """

    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller

        # set up start page window
        self.configure(bg="#EFF3F6")

        # Title label
        start_label = Label(text="แบบประเมินสติ ความหมกมุ่นครุ่นคิด และสุขภาวะทางอารมณ์",
                            font=("Sarabun", 20), borderwidth=2, relief="ridge")
        start_label.pack(side="left", padx=10, ipadx=5, ipady=3)

        # Main information text with additional left padding
        info_text = (
            "แบบประเมินทั้งหมดประกอบด้วย 2 ตอน\n"
            "ตอนที่ 1 แบบสอบถามสถานภาพของผู้ร่วมวิจัย จำนวน 3 ข้อ\n"
            "ตอนที่ 2 แบบประเมินทางจิตวิทยา ประกอบด้วย\n"
            "  1) แบบวัดสติประกอบด้วยแบบวัด 3 ฉบับ คือ\n"
            "     แบบวัด Mindful Attention Awareness Scale มีจำนวน 15 ข้อ\n"
            "     แบบวัด FFMQ จำนวน 24 ข้อ\n"
            "     แบบวัด PHLMS 20 ข้อ\n"
            "  2) แบบวัดความหมกมุ่นครุ่นคิด จำนวน 22 ข้อ\n"
            "  3) แบบวัดความไม่ยึดติดตัวตน จำนวน 7 ข้อ\n"
            "  4) แบบวัดการรับรู้ความเครียด จำนวน 14 ข้อ\n"
            "  5) แบบวัดสุขภาวะทางอารมณ์โดยรวม จำนวน 14 ข้อ\n\n"
        )
        info_label = Label(self, text=info_text, font=("Sarabun", 20), borderwidth=2, relief="ridge",
                           anchor="w", justify="left")
        info_label.pack(pady=10, padx=(30, 10), ipadx=20, ipady=3, fill="x")  # Added left padding with padx=(30, 10)

        # Purpose text with additional left padding
        purpose_text = ("กรุณาตอบตามความเป็นจริงและใช้เวลาในการตอบคำถามแต่ละข้ออย่างรวดเร็ว \n"
                        "**หลังจากกดเพื่อทำคำถามถัดไป ท่านไม่สามารถกลับมาแก้ไขคำตอบได้** \n"
                        "ขอบคุณสำหรับการเข้าร่วมในแบบประเมินของเรา")
        purpose_label = Label(self, text=purpose_text, font=("Sarabun", 20), borderwidth=2, relief="ridge",
                              anchor="w", justify="left")
        purpose_label.pack(pady=10, padx=(30, 10), ipadx=5, ipady=3, fill="x")  # Added left padding with padx=(30, 10)

        # Define the font
        custom_font = ("Sarabun", 20)

        # Create the button with the specified font
        start_button = ttk.Button(self, text="เริ่มต้นแบบสอบถาม",
                                  command=lambda: controller.show_frame(GenderQuestion),
                                  style="Custom.TButton")
        start_button.pack(ipadx=10, ipady=15, pady=15)

        # Configure the style
        s = ttk.Style()
        s.configure('.', font=custom_font)

        # Create the quit button
        quit_button = ttk.Button(self, text="ออกจากแบบสอบถาม", command=self.on_closing,
                                 style="Custom.TButton")
        quit_button.pack(ipady=3, pady=10)

    def on_closing(self):
        """
        Display dialog box before quitting.
        """
        if messagebox.askokcancel("ออก", "คุณต้องการออกจากแบบสอบถาม?"):
            self.controller.destroy()


class GenderQuestion(Frame):
    """
    Displays gender question from General questions.
    """

    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller

        global general_answers_list

        # Create a title label with font
        title_label = ttk.Label(self, text="แบบสอบถามสถานภาพของผู้ร่วมวิจัย", font=custom_font,
                                borderwidth=2, relief="ridge")
        title_label.pack(padx=10, pady=10)

        self.question = "เพศ"

        # Set up question label
        self.question_label = Label(self, text="1. {}".format(self.question), font=custom_font)
        self.question_label.pack(anchor='w', padx=20, pady=10)

        choices = [("หญิง", "Female"), ("ชาย", "Male"), ("ไม่ระบุ", "Other")]

        self.var = StringVar()
        self.var.set(0)  # Initialize

        # Style for the radio buttons
        style = ttk.Style()
        style.configure("Custom.TRadiobutton", font=custom_font)

        # Frame to contain radio buttons
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in choices:
            b = ttk.Radiobutton(checkbox_frame, text=text, variable=self.var, value=value, style="Custom.TRadiobutton")
            b.pack(fill='x', expand=True, ipadx=20, ipady=2)

        self.question_label.pack(anchor='w', padx=20, pady=20)
        Label(self, text="**หมายเหตุ หลังจากกดเพื่อทำคำถามถัดไป ท่านไม่สามารถกลับมาแก้ไขคำตอบได้**",
              font=custom_font).pack(padx=50, pady=20)
        self.question_label.pack(anchor='w', padx=20, pady=20)

        # Next question button with fo  nt
        enter_button = ttk.Button(self, text="คำถามถัดไป", command=self.nextQuestion)
        enter_button.pack(ipady=5, pady=20)

    def nextQuestion(self):
        '''
        When button is clicked, add user's input to a list
        and display next question.
        '''
        answer = self.var.get()

        if answer == '0':
            dialogBox("ไม่ได้กรอกแบบสอบถาม",
                      "คุณยังไม่ได้กรอกแบบสอบถาม\nโปรดกรอกแบบสอบถาม")
        else:
            selected_answer = self.var.get()
            general_answers_list.append(selected_answer)

            time.sleep(.2)  # delay between questions

            self.controller.show_frame(AgeQuestion)


class AgeQuestion(Frame):
    """
    Displays age question from General questions.
    """

    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        global general_answers_list

        # Create header label
        ttk.Label(self, text="แบบสอบถามสถานภาพของผู้ร่วมวิจัย", font=custom_font,
                  borderwidth=2, relief="ridge").pack(padx=10, pady=10)

        self.question = "คำชี้แจง โปรดทำเครื่องหมาย  ลงใน • หน้าข้อความหรือเติมรายละเอียดในช่องว่างที่ตรงกับสภาพความเป็นจริง"

        # Set up labels and age entry
        self.question_label = Label(self, text="2. อายุ...............ปี (หากไม่ต้องการระบุให้ข้ามไป)",
                                    font=custom_font)
        self.question_label.pack(anchor='w', padx=20, pady=10)

        # Age Entry
        self.age_var = StringVar()
        age_entry = ttk.Entry(self, textvariable=self.age_var, font=custom_font)
        age_entry.pack(pady=10, padx=50)

        # Skip button
        skip_button = ttk.Button(self, text="ข้าม", command=lambda: self.save_and_continue(skip=True))
        skip_button.pack(side='left', ipadx=10, ipady=5, pady=20, padx=20)

        # Next button
        next_button = ttk.Button(self, text="คำถามถัดไป", command=lambda: self.save_and_continue(skip=False))
        next_button.pack(side='right', ipadx=10, ipady=5, pady=20, padx=20)

    def save_and_continue(self, skip):
        """Save the user's input and continue to the next question"""
        age = self.age_var.get()

        if not age and not skip:
            dialogBox("คุณยังไม่ได้กรอกแบบสอบถาม", "โปรดกรอกอายุหรือกดข้าม")
        else:
            if skip:
                general_answers_list.append("Not Specified")
            else:
                general_answers_list.append(age)

            # print("Sex and Ages", general_answers_list)

            # Move to the next question or frame
            self.controller.show_frame(MindfulnessExperience)  # Replace with actual next frame


class MindfulnessExperience(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        global general_answers_list

        # Create header label
        ttk.Label(self, text="ประสบการณ์ในการฝึกสติ", font=custom_font,
                  borderwidth=2, relief="ridge").pack(padx=10, pady=10)

        # Experience Checkboxes
        self.never_practiced_var = IntVar()
        self.attended_course_var = IntVar()
        self.still_practicing_var = IntVar()
        self.not_practicing_var = IntVar()

        ttk.Label(self, text="1. ท่านเคยเข้ารับการอบรมฝึกสติหรือไม่", font=custom_font).pack(anchor='w', padx=20, pady=10)
        ttk.Checkbutton(self, text="ไม่เคยเข้าอบรมการฝึกสติเลย", variable=self.never_practiced_var).pack(anchor='w',
                                                                                                         padx=20,
                                                                                                         pady=5)
        ttk.Checkbutton(self,
                        text="เคยเข้าอบรมการฝึกสติ เช่น เข้าหลักสูตรปฏิบัติธรรมอย่างน้อย 3 วันที่สถานปฏิบัติธรรมติดกันขึ้นไป",
                        variable=self.attended_course_var).pack(anchor='w', padx=20, pady=5)

        # Detail Entry for "เคยเข้าอบรมการฝึกสติ"
        self.course_detail_var = StringVar()
        ttk.Label(self, text="โปรดระบุรายละเอียด", font=custom_font).pack(anchor='w', padx=40)
        ttk.Entry(self, textvariable=self.course_detail_var, width=50).pack(anchor='w', padx=40, pady=5)

        # Current Practice Checkboxes
        Label(self, text=" ", font=("Sarabun", 20)).pack(pady=10)
        ttk.Label(self, text="2. ปัจจุบันยังฝึกสติอยู่หรือไม่", font=custom_font).pack(anchor='w', padx=20, pady=10)
        ttk.Checkbutton(self, text="ยังฝึกอยู่", variable=self.still_practicing_var).pack(anchor='w', padx=40, pady=5)
        ttk.Checkbutton(self, text="ไม่ได้ฝึกแล้ว", variable=self.not_practicing_var).pack(anchor='w', padx=40, pady=5)

        # Next Button
        next_button = ttk.Button(self, text="คำถามถัดไป", command=self.save_and_continue)
        next_button.pack(pady=20)

    def save_and_continue(self):
        """Save the user's input and continue to the next question"""
        # Gather all responses into a dictionary or list
        response = {
            "never_practiced": self.never_practiced_var.get(),
            "attended_course": self.attended_course_var.get(),
            "course_detail": self.course_detail_var.get(),
            "still_practicing": self.still_practicing_var.get(),
            "not_practicing": self.not_practicing_var.get()
        }

        # Append response to the general answers list
        general_answers_list.append(response)

        # Check if no selection was made in question 1
        if self.never_practiced_var.get() == 0 and self.attended_course_var.get() == 0:
            dialogBox("ยังไม่ได้เลือกคำตอบ", "โปรดเลือกคำตอบข้อ 1 และลองอีกครั้ง")
            return  # Stop further processing

        # Check if no selection was made in question 2
        if self.attended_course_var.get() == 1 and (
                self.still_practicing_var.get() == 0 and self.not_practicing_var.get() == 0):
            dialogBox("ยังไม่ได้เลือกคำตอบ",
                      "หากเลือก 'เคยเข้าอบรมการฝึกสติ' \n "
                      "โปรดเลือกคำตอบข้อ 2 และลองอีกครั้ง")
            return

        # Check if multiple selections were made in question 1
        if self.never_practiced_var.get() == 1 and self.attended_course_var.get() == 1:
            dialogBox("คุณตอบข้อที่ 1 เกิน 1 ตัวเลือก", "กรุณาเลือกเพียงหนึ่งคำตอบเท่านั้น")
            return

        # Check if multiple selections were made in question 2
        if self.still_practicing_var.get() == 1 and self.not_practicing_var.get() == 1:
            dialogBox("คุณตอบข้อที่ 2 เกิน 1 ตัวเลือก", "กรุณาเลือกเพียงหนึ่งคำตอบเท่านั้น")
            return

        # Move to the next frame based on the "ยังฝึกอยู่" checkbox
        if self.still_practicing_var.get() == 1:
            self.controller.show_frame(MindfulnessExperienceDetail)  # Show the detail page if "ยังฝึกอยู่" is selected
        else:
            self.controller.show_frame(MindfulAttentionAwarenessScale)  # Else, proceed to the next main section

class MindfulnessExperienceDetail(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Frequency and Duration Variables
        self.daily_var = IntVar()
        self.weekly_var = IntVar()
        self.monthly_var = IntVar()
        self.yearly_var = IntVar()

        self.daily_count = StringVar()
        self.weekly_count = StringVar()
        self.monthly_count = StringVar()
        self.yearly_count = StringVar()

        self.daily_duration = StringVar()
        self.weekly_duration = StringVar()
        self.monthly_duration = StringVar()
        self.yearly_duration = StringVar()

        # Label for Instruction
        ttk.Label(self, text="ถ้ายังฝึกปฏิบัติอยู่ ท่านฝึกบ่อยแค่ไหน (โปรดระบุความถี่)", font=custom_font, anchor="w").pack(anchor='w', padx=20, pady=5)

        # Daily Frequency Line
        daily_frame = ttk.Frame(self)
        daily_frame.pack(anchor='w', padx=40, pady=5)
        ttk.Checkbutton(daily_frame, text="รายวัน", variable=self.daily_var).pack(side='left')
        ttk.Entry(daily_frame, textvariable=self.daily_count, width=10).pack(side='left', padx=(15, 5))
        ttk.Label(daily_frame, text="ครั้ง/วัน").pack(side='left', padx=(5, 15))
        ttk.Entry(daily_frame, textvariable=self.daily_duration, width=10).pack(side='left', padx=(15, 5))
        ttk.Label(daily_frame, text="ครั้งละ/นาที").pack(side='left', padx=(5, 0))

        # Weekly Frequency Line
        weekly_frame = ttk.Frame(self)
        weekly_frame.pack(anchor='w', padx=40, pady=5)
        ttk.Checkbutton(weekly_frame, text="รายสัปดาห์", variable=self.weekly_var).pack(side='left')
        ttk.Entry(weekly_frame, textvariable=self.weekly_count, width=10).pack(side='left', padx=(15, 5))
        ttk.Label(weekly_frame, text="ครั้ง/สัปดาห์").pack(side='left', padx=(5, 15))
        ttk.Entry(weekly_frame, textvariable=self.weekly_duration, width=10).pack(side='left', padx=(15, 5))
        ttk.Label(weekly_frame, text="ครั้งละ/นาที").pack(side='left', padx=(5, 0))

        # Monthly Frequency Line
        monthly_frame = ttk.Frame(self)
        monthly_frame.pack(anchor='w', padx=40, pady=5)
        ttk.Checkbutton(monthly_frame, text="รายเดือน", variable=self.monthly_var).pack(side='left')
        ttk.Entry(monthly_frame, textvariable=self.monthly_count, width=10).pack(side='left', padx=(15, 5))
        ttk.Label(monthly_frame, text="ครั้ง/เดือน").pack(side='left', padx=(5, 15))
        ttk.Entry(monthly_frame, textvariable=self.monthly_duration, width=10).pack(side='left', padx=(15, 5))
        ttk.Label(monthly_frame, text="ครั้งละ/นาที").pack(side='left', padx=(5, 0))

        # Yearly Frequency Line
        yearly_frame = ttk.Frame(self)
        yearly_frame.pack(anchor='w', padx=40, pady=5)
        ttk.Checkbutton(yearly_frame, text="รายปี", variable=self.yearly_var).pack(side='left')
        ttk.Entry(yearly_frame, textvariable=self.yearly_count, width=10).pack(side='left', padx=(15, 5))
        ttk.Label(yearly_frame, text="ครั้ง/ปี").pack(side='left', padx=(5, 15))
        ttk.Entry(yearly_frame, textvariable=self.yearly_duration, width=10).pack(side='left', padx=(15, 5))
        ttk.Label(yearly_frame, text="ครั้งละ/นาที").pack(side='left', padx=(5, 0))

        # Mindfulness Practice Types Checkboxes
        ttk.Label(self, text="รูปแบบของการฝึกสติ", font=custom_font, anchor="w").pack(anchor='w', padx=20, pady=10)
        self.anapanasati_var = IntVar()
        self.yub_pong_var = IntVar()
        self.metta_var = IntVar()
        self.watch_mind_var = IntVar()
        self.asubha_var = IntVar()
        self.other_var = StringVar()

        ttk.Checkbutton(self, text="ดูลมหายใจ (อานาปานสติ)", variable=self.anapanasati_var).pack(anchor='w', padx=40, pady=5)
        ttk.Checkbutton(self, text="ยุบหนอ-พองหนอ", variable=self.yub_pong_var).pack(anchor='w', padx=40, pady=5)
        ttk.Checkbutton(self, text="เมตตาภาวนา", variable=self.metta_var).pack(anchor='w', padx=40, pady=5)
        ttk.Checkbutton(self, text="ดูจิต", variable=self.watch_mind_var).pack(anchor='w', padx=40, pady=5)
        ttk.Checkbutton(self, text="เจริญอสุภกรรมฐาน", variable=self.asubha_var).pack(anchor='w', padx=40, pady=5)

        # Entry for "อื่นๆ"
        ttk.Label(self, text="อื่นๆ โปรดระบุ", font=custom_font, anchor="w").pack(anchor='w', padx=40, pady=5)
        ttk.Entry(self, textvariable=self.other_var, width=50).pack(anchor='w', padx=40, pady=5)


        Label(self, text="**หมายเหตุ หลังจากกดเพื่อทำคำถามถัดไป ท่านไม่สามารถกลับมาแก้ไขคำตอบได้**",
              font=custom_font).pack(padx=50, pady=20)

        # Next Button
        next_button = ttk.Button(self, text="คำถามถัดไป", command=self.save_and_proceed)
        next_button.pack(anchor='center', pady=20)

    def save_and_proceed(self):
        """Save the user's input from this page and go to the next frame"""
        # Ensure at least one practice type is selected or "อื่นๆ" is filled
        if not (self.anapanasati_var.get() or self.yub_pong_var.get() or self.metta_var.get() or
                self.watch_mind_var.get() or self.asubha_var.get() or self.other_var.get().strip()):
            messagebox.showwarning("Incomplete Input", "โปรดเลือกอย่างน้อย 1 รูปแบบของการฝึกสติหรือระบุใน 'อื่นๆ'")
            return  # Stop execution if the validation fails

        # Save the responses
        additional_response = {
            "daily": {"enabled": self.daily_var.get(), "count": self.daily_count.get(),
                      "duration": self.daily_duration.get()},
            "weekly": {"enabled": self.weekly_var.get(), "count": self.weekly_count.get(),
                       "duration": self.weekly_duration.get()},
            "monthly": {"enabled": self.monthly_var.get(), "count": self.monthly_count.get(),
                        "duration": self.monthly_duration.get()},
            "yearly": {"enabled": self.yearly_var.get(), "count": self.yearly_count.get(),
                       "duration": self.yearly_duration.get()},
            "anapanasati": self.anapanasati_var.get(),
            "yub_pong": self.yub_pong_var.get(),
            "metta": self.metta_var.get(),
            "watch_mind": self.watch_mind_var.get(),
            "asubha": self.asubha_var.get(),
            "other": self.other_var.get()
        }

        general_answers_list[-1].update(additional_response)  # Update the last entry with additional details

        # Proceed to the next main section
        self.controller.show_frame(MindfulAttentionAwarenessScale)


class MindfulAttentionAwarenessScale(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller
        global MAA_list

        # Create header label
        ttk.Label(self, text=(
            "คำแนะนำ: ข้อความด้านล่างเป็นประโยคที่เกี่ยวกับประสบการณ์ในชีวิตประจำวันของท่าน\n"
            "กรุณาใช้มาตรวัด 1-6 ด้านล่างเพื่อระบุถึงความบ่อยของประสบการณ์แต่ละเรื่องเร็วๆ นี้ของท่าน\n"
            "\n"
            "กรุณาตอบตามความเป็นจริงตามประสบการณ์ของท่านมากกว่าการคิดว่าควรจะตอบอย่างไร\n"
            "กรุณาประเมินข้อความแต่ละข้อแบบแยกจากกัน"), font=custom_font,
            borderwidth=2, relief="ridge").pack(padx=10, pady=10)

        Label(self, text=" ", font=("Sarabun", 20)).pack(pady=10)

        Label(self, text="**หมายเหตุ หลังจากกดเพื่อทำคำถามถัดไป ท่านไม่สามารถกลับมาแก้ไขคำตอบได้**",
              font=custom_font).pack(padx=50, pady=20)

        self.questions = [
            "ฉันอาจเคยสัมผัสกับอารมณ์บางอย่าง แต่ไม่สามารถรู้สึกถึงมันได้จนกว่ามันผ่านไปแล้ว",
            "ฉันทำสิ่งของแตกหักเพราะความประมาท. ไม่ได้ใส่ใจ หรือคิดถึงสิ่งอื่นอยู่",
            "ฉันพบว่า มันยุ่งยากที่จะคงอยู่กับสิ่งที่เกิดขึ้นกับปัจจุบัน",
            "ฉันมักเดินอย่างรวดเร็วไปยังที่หมายโดยไม่ได้ใส่ใจสิ่งที่พบเจอระหว่างทาง",
            "ฉันมักไม่ได้สังเกตถึงความรู้สึกตึงเครียดหรือความไม่สบายทางร่างกาย จนกว่ามันจะดึงความใส่ใจของฉัน",
            "ฉันลืมชื่อคนในเกือบจะทันที่ที่ฉันถูกบอกในครั้งแรก",
            "มันเหมือนกับว่าฉัน “ทำไปอย่างอัตโนมัติ” โดยไม่รู้ตัวมากนักในสิ่งที่ฉันกำลังทำ",
            "ฉันรีบทำกิจกรรมต่าง ๆ โดยไม่ได้เอาใจใส่มันอย่างแท้จริง",
            "ฉันเพ่งความสนใจไปยังเป้าหมายที่ต้องการโดยขาดการเชื่อมต่อระหว่างสิ่งที่ฉันกำลังทำอยู่ในปัจจุบันกับจุดหมายนั้น",
            "ฉันทำงานหรือภารกิจไปแบบอัตโนมัติโดยไม่รู้ตัวว่ากำลังทำอะไรอยู่",
            "ฉันพบว่า ตัวเองฟังบางคนแบบเข้าหูซ้ายทะลุหูขวา และทำสิ่งอื่นในเวลาเดียวกัน",
            "ฉันขับขี่รถไปที่ต่าง ๆ ด้วย “ระบบอัตโนมัติ” แล้วก็สงสัยว่าฉันไปที่นั่นทำไม",
            "ฉันพบว่า ตัวฉันมักถูกครอบงำด้วยเรื่องในอนาคตหรืออดีต",
            "ฉันพบว่า ตัวฉันทำสิ่งต่าง ๆ โดยไม่ใส่ใจ",
            "ฉันกินของขบเคี้ยวโดยไม่รู้ตัวว่ากำลังกิน"
        ]

        # Set index in questions list
        self.index = 0
        self.length_of_list = len(self.questions)

        Label(self, text=" ", font=("Sarabun", 20)).pack()
        self.question_label = Label(self, text="{}. {}".format(self.index + 1, self.questions[self.index]),
                                    font=custom_font)
        self.question_label.pack(anchor='w', padx=20, pady=20)

        Label(self, text="ระดับคะแนนและความหมาย", font=custom_font).pack(padx=50, pady=20)

        # Scale descriptions
        scale_text = ["เกือบสม่ำเสมอ", "บ่อยมาก", "บ่อย", "ไม่บ่อย", "นาน ๆ ครั้ง", "แทบจะไม่เคย"]
        scale_values = [("1", 1), ("2", 2), ("3", 3), ("4", 4), ("5", 5), ("6", 6)]
        self.var = StringVar()
        self.var.set(0)  # initialize

        # Create a frame for the scale table
        scale_frame = Frame(self, borderwidth=2, relief="ridge")
        scale_frame.pack(pady=10, padx=20)

        # Add descriptions in the first row of the table
        for col, text in enumerate(scale_text):
            label = Label(scale_frame, text=text, font=("Sarabun", 20))
            label.grid(row=0, column=col, padx=15, pady=10, sticky='n')

        # Add radio buttons in the second row of the table
        for col, (text, value) in enumerate(scale_values):
            radio = Radiobutton(scale_frame, text=text, variable=self.var, value=value, font=("Sarabun", 18))
            radio.grid(row=1, column=col, padx=15, pady=20)

        # Create next question button
        next_button = ttk.Button(self, text="คำถามถัดไป", command=self.nextQuestion)
        next_button.pack(ipady=5, pady=20)

    def nextQuestion(self):
        """
        When button is clicked, add user's input to a list
        and display the next question or end the survey.
        """
        answer = self.var.get()

        if answer == '0':
            dialogBox("ยังไม่ได้เลือกคำตอบ", "โปรดเลือกคำตอบ\nลองอีกครั้ง")
        elif self.index == (self.length_of_list - 1):
            # Get the last answer from the user
            selected_answer = self.var.get()
            MAA_list.append(selected_answer)

            # Disable interactive widgets before showing the dialog
            for widget in self.winfo_children():
                try:
                    widget.configure(state='disabled')
                except TclError:
                    # Ignore widgets that don't have a state option
                    pass

            # Show the dialog box for the next survey
            next_survey_text = "จบแบบวัด MAAS \n \n \n กด เริ่ม เพื่อเริ่มทำแบบวัด FFMQ-SF"
            nextSurveyDialog(
                "แบบสอบถามถัดไป",
                next_survey_text,
                lambda: self.controller.show_frame(FFMQ_SF)
            )
        else:
            self.index = (self.index + 1) % self.length_of_list

            # Update the question label
            self.question_label.config(text="{}. {}".format(self.index + 1, self.questions[self.index]))

            # Save the current answer
            selected_answer = self.var.get()
            MAA_list.append(selected_answer)

            # Reset value for the next question
            self.var.set(0)

            # Optional: Add a short delay for smoother transition
            time.sleep(0.2)


class FFMQ_SF(Frame):
    """
    Class that displays the window for the significant consumption trends survey questions.
    When the user answers a question, the answer is written to a
    csv file.
    """

    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller

        global FFMQ_SF_list

        # Create header label
        ttk.Label(self, text="โปรดอ่านข้อความ แล้วเลือกตัวเลขที่ตรงกับความเป็นจริงของท่านที่สุดในช่วง 2 สัปดาห์ที่ผ่านมา", font=custom_font,
                  borderwidth=2, relief="ridge").pack(padx=10, pady=10)
        Label(self, text=" ", font=("Sarabun", 20)).pack(pady=10)

        Label(self, text="**หมายเหตุ หลังจากกดเพื่อทำคำถามถัดไป ท่านไม่สามารถกลับมาแก้ไขคำตอบได้**",
              font=custom_font).pack(padx=50, pady=20)

        self.questions = [
                        "ฉันสามารถหาคำพูดมาอธิบายความรู้สึกของฉันได้โดยไม่ยาก",
                        "ฉันสามารถอธิบายความคิด ความเชื่อ และความคาดหวังของฉันออกมาเป็นคำพูดให้คนอื่นเข้าใจได้ง่าย",
                        "ฉันติดตามเฝ้าดูความรู้สึกของฉันได้โดยไม่หลงเข้าไปในความรู้สึกนั้น",
                        "ฉันบอกตัวเองว่า ฉันไม่ควรมีความรู้สึกอย่างที่กำลังรู้สึกอยู่",
                        "เป็นการยากที่จะอธิบายความคิดของฉันออกมาเป็นคำพูด",
                        "ฉันใส่ใจในสัมผัสต่างๆ เช่น เมื่อลมต้องผมของฉัน หรือแสงอาทิตย์ที่ส่องบนใบหน้าของฉัน",
                        "ฉันมักตัดสินความคิดของฉันว่า ดีหรือไม่ดี",
                        "ฉันพบว่า ฉันบังคับตัวเองให้สนใจในสิ่งที่กำลังเกิดขึ้นในปัจจุบันได้ยาก",
                        "เมื่อเกิดความวิตกกังวล ฉันไม่ให้ความวิตกกังวลนั้นครอบงำฉันได้",
                        "โดยปกติฉันมีความสนใจต่อเสียงรอบข้าง เช่น เสียงนาฬิกาเดิน เสียงนกร้อง เสียงรถแล่น",
                        "เมื่อฉันรับรู้ถึงความรู้สึกบางอย่างที่เกิดขึ้นกับร่างกายของฉัน ฉันไม่สามารถหาคำพูดที่เหมาะสมเพื่ออธิบายอาการนั้นได้",
                        "มันเหมือนกับว่า “ฉันทำทุกอย่างไปตามอัตโนมัติ” โดยไม่รู้ว่ากำลังทำอะไรอยู่",
                        "เมื่อเกิดความวิตกกังวล หลังจากนั้นไม่นาน ฉันรู้สึกสงบลงได้",
                        "ฉันบอกกับตัวเองว่า ฉันไม่ควรคิดแบบที่คิดอยู่นั้นเลย",
                        "ฉันรับรู้ถึงกลิ่นและความหอมของสิ่งต่าง ๆ ได้",
                        "แม้ในขณะที่ฉันกำลังโกรธ ฉันก็สามารถอธิบายความรู้สึกออกมาเป็นคำพูดได้",
                        "ฉันเร่งรีบทำกิจกรรมต่าง ๆ โดยไม่ได้มีความใส่ใจในสิ่งที่ทำอย่างแท้จริง",
                        "เมื่อฉันเกิดความวิตกกังวล ฉันสามารถรับรู้ความวิตกกังวลนั้นได้โดยไม่มีปฏิกิริยาตอบสนอง",
                        "ฉันคิดว่า อารมณ์บางอย่างของฉันแย่และไม่เหมาะสม และฉันก็ไม่ควรมีอารมณ์เช่นนั้น",
                        "ฉันสังเกตเห็นองค์ประกอบของภาพในงานศิลปะหรือธรรมชาติ เช่น สี รูปร่าง รายละเอียดหรือแนวของแสงและเงา",
                        "เมื่อฉันเกิดความวิตกกังวล ฉันสามารถรับรู้ถึงความรู้สึกนั้นและปล่อยผ่านไปได้",
                        "ฉันทำงานหรือปฏิบัติหน้าที่ต่าง ๆ อย่างอัตโนมัติโดยไม่ค่อยรู้ตัวว่ากำลังทำอะไรอยู่",
                        "ฉันพบว่า ฉันทำสิ่งต่าง ๆ โดยไม่ได้ใส่ใจในสิ่งนั้น (ทำไปอย่างนั้นเอง)",
                        "ฉันไม่ยอมรับตัวเองเมื่อมีความคิดที่ไม่เหมาะสม"
                    ]

        # Set index in questions list
        self.index = 0
        self.length_of_list = len(self.questions)

        # Display the question
        Label(self, text=" ", font=("Sarabun", 20)).pack()
        self.question_label = Label(self, text="{}. {}".format(self.index + 1, self.questions[self.index]),
                                    font=custom_font)
        self.question_label.pack(anchor='w', padx=20, pady=20)

        Label(self, text="ระดับคะแนนและความหมาย", font=custom_font).pack(padx=50, pady=20)

        # Scale descriptions and values
        scale_text = ["ไม่จริงเลย", "ไม่ค่อยจริง", "จริงบางครั้ง", "ค่อนข้างจริง", "จริงที่สุด"]
        scale_values = [("1", 1), ("2", 2), ("3", 3), ("4", 4), ("5", 5)]
        self.var = StringVar()
        self.var.set(0)  # initialize

        # Create a frame for the scale table
        scale_frame = Frame(self, borderwidth=2, relief="ridge")
        scale_frame.pack(pady=10, padx=20)

        # Add descriptions in the first row of the table
        for col, text in enumerate(scale_text):
            label = Label(scale_frame, text=text, font=("Sarabun", 20))
            label.grid(row=0, column=col, padx=15, pady=10, sticky='n')

        # Add radio buttons in the second row of the table with larger font for numbers
        for col, (text, value) in enumerate(scale_values):
            radio = Radiobutton(scale_frame, text=text, variable=self.var, value=value, font=("Sarabun", 18))
            radio.grid(row=1, column=col, padx=15, pady=20)

        # Create next question button
        enter_button = ttk.Button(self, text="คำถามถัดไป", command=self.nextQuestion)
        enter_button.pack(ipady=5, pady=20)

    def nextQuestion(self):
        '''
        When button is clicked, add user's input to a list
        and display next question.
        '''
        answer = self.var.get()

        if answer == '0':
            dialogBox("ยังไม่ได้ตอบคำถาม",
                      "โปรดตอบคำถาม.\nและลองใหม่อีกครั้ง.")
        elif self.index == (self.length_of_list - 1):
            # get the last answer from user
            selected_answer = self.var.get()
            FFMQ_SF_list.append(selected_answer)
            print("FFMQ_SF", FFMQ_SF_list)

            # Disable interactive widgets before showing the dialog
            for widget in self.winfo_children():
                try:
                    widget.configure(state='disabled')
                except TclError:
                    pass  # Ignore widgets that don't have a state option

            next_survey_text = "จบแบบวัด FFMQ-SF \n \n \n กด เริ่ม เพื่อเริ่มทำแบบวัด PHLMS"
            nextSurveyDialog("แบบสอบถามถัดไป", next_survey_text,
                             lambda: self.controller.show_frame(PHLMS))
        else:
            self.index = (self.index + 1) % self.length_of_list

            self.question_label.config(text="{}. {}".format(self.index + 1, self.questions[self.index]))
            selected_answer = self.var.get()
            FFMQ_SF_list.append(selected_answer)

            self.var.set(0)  # reset value for next question
            time.sleep(.2)  # delay between questions


class PHLMS(Frame):
    """
    Class that displays the window for the future consumption trends survey questions.
    When the user answers a question, the answer is written to a
    csv file.
    """

    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller

        global PHLMS_list

        # Create header label
        ttk.Label(self, text="คำชี้แจง : โปรดอ่านข้อความ แล้วเลือกตัวเลขที่ตรงกับความเป็นจริงของท่านที่สุดในช่วง 1 สัปดาห์ที่ผ่านมา", font=custom_font,
                  borderwidth=2, relief="ridge").pack(padx=10, pady=10)
        Label(self, text=" ", font=("Sarabun", 20)).pack(pady=10)

        Label(self, text="**หมายเหตุ หลังจากกดเพื่อทำคำถามถัดไป ท่านไม่สามารถกลับมาแก้ไขคำตอบได้**",
              font=custom_font).pack(padx=50, pady=20)

        self.questions = [
                    "ฉันตระหนักรู้ว่า มีความคิดอะไรผ่านเข้ามาในใจบ้าง",
                    "ฉันพยายามเบี่ยงเบนตนเองไป เวลาที่ฉันมีความรู้สึกไม่สบอารมณ์",
                    "เวลาที่ฉันพูดคุยกับคนอื่น ฉันตระหนักรู้การแสดงออกทางสีหน้าและท่าทางของเขา",
                    "มีแง่มุมบางอย่างเกี่ยวกับตัวฉันเองที่ฉันไม่ต้องการคิดถึงมัน",
                    "เวลาฉันอาบน้ำ ฉันตระหนักรู้ว่าน้ำไหลผ่านผิวกายของฉันอย่างไร",
                    "ฉันพยายามทำตัวให้ยุ่ง ๆ เพื่อไม่ให้ความคิดหรือความรู้สึกเข้ามาในใจ",
                    "เมื่อฉันตกใจ ฉันสังเกตว่ามีอะไรเกิดขึ้นภายในร่างกายของฉัน",
                    "ฉันปรารถนาว่า ฉันจะควบคุมอารมณ์ของฉันได้ง่ายขึ้น",
                    "เมื่อฉันเดินอยู่ข้างนอก ฉันตระหนักรู้ลมหรือกลิ่นที่สัมผัสใบหน้าของฉันได้",
                    "ฉันบอกกับตัวเองว่า ฉันไม่ควรจะมีความคิดบางอย่าง",
                    "เมื่อมีใครถามว่าฉันรู้สึกอย่างไร ฉันสามารถระบุอารมณ์ของฉันโดยง่าย",
                    "มีหลายสิ่งที่ฉันพยายามไม่คิดถึงมัน",
                    "ฉันตระหนักรู้ความคิดที่ฉันกำลังมีอยู่ขณะที่อารมณ์ของฉันเปลี่ยนแปลง",
                    "ฉันบอกกับตัวเองว่า ฉันไม่ควรรู้สึกโศกเศร้าเสียใจ",
                    "ฉันสังเกตการเปลี่ยนแปลงในร่างกาย เช่น หัวใจเต้นเร็วหรือกล้ามเนื้อเกร็ง",
                    "หากว่ามีบางสิ่งที่ฉันไม่อยากคิดถึงมัน ฉันจะพยายามหลายอย่างที่จะขจัดมันออกไปจากใจของฉัน",
                    "เมื่อไหร่ก็ตามที่อารมณ์ของฉันเปลี่ยนแปลง ฉันจะระลึกรู้ได้ทันที",
                    "ฉันพยายามผลักปัญหาต่าง ๆ ออกไปจากใจ",
                    "เมื่อกำลังพูดคุยกับคนอื่น ฉันตระหนักรู้อารมณ์ที่ฉันกำลังประสบอยู่ได้",
                    "เมื่อฉันมีความจำที่เลวร้าย ฉันพยายามเบี่ยงเบนตัวเองไปเพื่อไม่คิดถึงมัน"
                ]

        # Set index in questions list
        self.index = 0
        self.length_of_list = len(self.questions)

        # Display the question
        Label(self, text=" ", font=("Sarabun", 20)).pack()
        self.question_label = Label(self, text="{}. {}".format(self.index + 1, self.questions[self.index]),
                                    font=custom_font)
        self.question_label.pack(anchor='w', padx=20, pady=20)

        Label(self, text="ระดับคะแนนและความหมาย", font=custom_font).pack(padx=50, pady=20)

        # Scale descriptions and values
        scale_text = ["ไม่เคยเลย", "นาน ๆ ครั้ง", "บางครั้ง", "บ่อย ๆ", "บ่อยมาก"]
        scale_values = [("1", 1), ("2", 2), ("3", 3), ("4", 4), ("5", 5)]
        self.var = StringVar()
        self.var.set(0)  # initialize

        # Create a frame for the scale table
        scale_frame = Frame(self, borderwidth=2, relief="ridge")
        scale_frame.pack(pady=10, padx=20)

        # Add descriptions in the first row of the table
        for col, text in enumerate(scale_text):
            label = Label(scale_frame, text=text, font=("Sarabun", 20))
            label.grid(row=0, column=col, padx=15, pady=10, sticky='n')

        # Add radio buttons in the second row of the table with larger font for numbers
        for col, (text, value) in enumerate(scale_values):
            radio = Radiobutton(scale_frame, text=text, variable=self.var, value=value, font=("Sarabun", 18))
            radio.grid(row=1, column=col, padx=15, pady=20)

        # Create next question button
        enter_button = ttk.Button(self, text="คำถามถัดไป", command=self.nextQuestion)
        enter_button.pack(ipady=5, pady=20)

    def nextQuestion(self):
        '''
        When button is clicked, add user's input to a list
        and display next question.
        '''
        answer = self.var.get()

        if answer == '0':
            dialogBox("ยังไม่ได้ตอบคำถาม",
                      "โปรดตอบคำถาม.\nและลองใหม่อีกครั้ง.")
        elif self.index == (self.length_of_list - 1):
            # get the last answer from user
            selected_answer = self.var.get()

            PHLMS_list.append(selected_answer)
            print("PHLMS", PHLMS_list)

            # Disable interactive widgets before showing the dialog
            for widget in self.winfo_children():
                try:
                    widget.configure(state='disabled')
                except TclError:
                    pass  # Ignore widgets that don't have a state option

            next_survey_text = "จบแบบวัด PHLMS \n \n \n กด เริ่ม เพื่อเริ่มทำแบบวัด Ruminative Thinking Scale"
            nextSurveyDialog("แบบสอบถามถัดไป", next_survey_text, lambda: self.controller.show_frame(RuminativeThinkingScale))
        else:
            self.index = (self.index + 1) % self.length_of_list

            self.question_label.config(text="{}. {}".format(self.index + 1, self.questions[self.index]))
            selected_answer = self.var.get()

            PHLMS_list.append(selected_answer)

            self.var.set(0)  # reset value for next question

            time.sleep(.2)  # delay between questions


class RuminativeThinkingScale(Frame):
    """
    Class that displays the window for the future consumption trends survey questions.
    When the user answers a question, the answer is written to a
    csv file.
    """

    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller

        global RuminativeThinking_list

        # Create header label
        ttk.Label(self, text="ผู้คนมีความคิดและการกระทำสิ่งต่าง ๆ ที่แตกต่างกันเมื่อรู้สึกซึมเศร้า \n \n"
                            "กรุณาอ่านข้อความแต่ละข้อแล้วระบุว่าท่านแทบจะไม่เคย บางครั้ง บ่อยครั้ง \n "
                            "หรือแทบจะทุกครั้งที่คิดหรือกระทำตามข้อความในแต่ละข้อ เมื่อท่านรู้สึกแย่ เศร้าเสียใจหรือซึมเศร้า \n \n"
                            "กรุณาเลือกสิ่งที่ท่านทำโดยทั่วไปไม่ใช่สิ่งที่ท่านคิดว่าท่านควรกระทำ \n",
                    borderwidth=2, relief="ridge").pack(padx=10, pady=10)
        # Label(self, text=" ", font=("Sarabun", 20)).pack(pady=10)

        Label(self, text="**หมายเหตุ หลังจากกดเพื่อทำคำถามถัดไป ท่านไม่สามารถกลับมาแก้ไขคำตอบได้**",
              font=custom_font).pack(padx=50, pady=20)

        self.questions = [
                    "คิดว่า ท่านโดดเดี่ยวเพียงใด",
                    "คิดว่า “ฉันจะทำงานไม่ได้ถ้าฉันไม่หลุดจากความวิตกกังวลนี้",
                    "คิดเกี่ยวกับความรู้สึกเหนื่อยล้าและเจ็บปวด",
                    "คิดว่า มันยากเพียงใดที่จะมีสมาธิจดจ่อ",
                    "คิดว่า “ฉันทำอะไรจึงสมควรได้รับสิ่งนี้?",
                    "คิดว่า คุณรู้สึกนิ่งเฉยและขาดแรงจูงใจเพียงใด",
                    "วิเคราะห์เหตุการณ์ในช่วงนี้เพื่อพยายามเข้าใจว่าทำไมคุณจึงรู้สึกหม่นหมอง",
                    "คิดว่า คุณไม่มีความรู้สึกใดๆ อีกต่อไป",
                    "คิดว่า “ทำไมฉันจึงเริ่มต้นไม่ได้?",
                    "คิดว่า “ทำไมฉันมักจะทำแบบนี้เสมอ?",
                    "ออกมาอยู่กับตัวเองและคิดว่าทำไมคุณจึงรู้สึกแบบนี้",
                    "เขียนสิ่งที่คุณกำลังคิดและลองวิเคราะห์ดู",
                    "คิดเกี่ยวกับสถานการณ์ที่เกิดขึ้นเร็ว ๆ นี้และอยากให้มันดีขึ้น",
                    "คิดว่า “ฉันไม่สามารถมีสมาธิจดจ่อได้หากฉันยังคงรู้สึกแบบนี้",
                    "คิดว่า “ทำไมฉันมีปัญหาที่ใคร ๆ เขาไม่มี?",
                    "คิดว่า “ทำไมฉันไม่สามารถจัดการสิ่งต่างๆ ได้ดีกว่านี้?",
                    "คิดว่า คุณเศร้ามากแค่ไหน",
                    "คิดถึงความบกพร่อง ความล้มเหลว ความผิดพลาดต่าง ๆ ของคุณ",
                    "คิดว่าคุณไม่มีกำลังใจพอที่จะทำอะไรเลย",
                    "วิเคราะห์บุคลิกภาพของคุณเพื่อพยายามเข้าใจว่าทำไมคุณจึงรู้สึกซึมเศร้า",
                    "ไปที่สักแห่งเพียงลำพังเพื่อครุ่นคิดถึงความรู้สึกของคุณ",
                    "คิดว่าคุณโกรธตัวเองมากเพียงใด"
                ]

        # Set index in questions list
        self.index = 0
        self.length_of_list = len(self.questions)

        # Display the question
        Label(self, text=" ", font=("Sarabun", 20)).pack()
        self.question_label = Label(self, text="{}. {}".format(self.index + 1, self.questions[self.index]),
                                    font=custom_font)
        self.question_label.pack(anchor='w', padx=20, pady=20)

        Label(self, text="ระดับคะแนนและความหมาย", font=custom_font).pack(padx=50, pady=20)

        # Scale descriptions and values
        scale_text = ["แทบจะไม่เคย", "บางครั้ง", "บ่อยครั้ง", "แทบจะทุกครั้ง"]
        scale_values = [("1", 1), ("2", 2), ("3", 3), ("4", 4)]
        self.var = StringVar()
        self.var.set(0)  # initialize

        # Create a frame for the scale table
        scale_frame = Frame(self, borderwidth=2, relief="ridge")
        scale_frame.pack(pady=10, padx=20)

        # Add descriptions in the first row of the table
        for col, text in enumerate(scale_text):
            label = Label(scale_frame, text=text, font=("Sarabun", 20))
            label.grid(row=0, column=col, padx=15, pady=10, sticky='n')

        # Add radio buttons in the second row of the table with larger font for numbers
        for col, (text, value) in enumerate(scale_values):
            radio = Radiobutton(scale_frame, text=text, variable=self.var, value=value, font=("Sarabun", 18))
            radio.grid(row=1, column=col, padx=15, pady=20)

        # Create next question button
        enter_button = ttk.Button(self, text="คำถามถัดไป", command=self.nextQuestion)
        enter_button.pack(ipady=5, pady=20)

    def nextQuestion(self):
        '''
        When button is clicked, add user's input to a list
        and display next question.
        '''
        answer = self.var.get()

        if answer == '0':
            dialogBox("ยังไม่ได้ตอบคำถาม",
                      "โปรดตอบคำถาม.\nและลองใหม่อีกครั้ง.")
        elif self.index == (self.length_of_list - 1):
            # get the last answer from user
            selected_answer = self.var.get()

            RuminativeThinking_list.append(selected_answer)
            print("RuminativeThinking", RuminativeThinking_list)

            # Disable interactive widgets before showing the dialog
            for widget in self.winfo_children():
                try:
                    widget.configure(state='disabled')
                except TclError:
                    pass  # Ignore widgets that don't have a state option

            next_survey_text = "จบแบบวัดความหมกมุ่นครุ่นคิด \n \n \n กด เริ่ม เพื่อเริ่มทำแบบวัด Non-Attachment To Self"
            nextSurveyDialog("แบบสอบถามถัดไป", next_survey_text, lambda: self.controller.show_frame(NonAttachmentToSelf))
        else:
            self.index = (self.index + 1) % self.length_of_list

            self.question_label.config(text="{}. {}".format(self.index + 1, self.questions[self.index]))
            selected_answer = self.var.get()

            RuminativeThinking_list.append(selected_answer)

            self.var.set(0)  # reset value for next question

            time.sleep(.2)  # delay between questions


class NonAttachmentToSelf(Frame):
    """
    Class that displays the window for the future consumption trends survey questions.
    When the user answers a question, the answer is written to a
    csv file.
    """

    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller

        global NonAttachmentToSelf_list

        # Create header label
        ttk.Label(self, text="โปรดอ่านข้อความ แล้วเลือกตัวเลขที่ตรงกับความเป็นจริงของท่านที่สุด",
                    borderwidth=2, relief="ridge").pack(padx=10, pady=10)
        Label(self, text=" ", font=("Sarabun", 20)).pack(pady=10)

        Label(self, text="**หมายเหตุ หลังจากกดเพื่อทำคำถามถัดไป ท่านไม่สามารถกลับมาแก้ไขคำตอบได้**",
              font=custom_font).pack(padx=50, pady=20)

        self.questions = [
                "ฉันปล่อยวางความคิดที่ไม่เป็นประโยชน์กับตัวเองได้",
                "ฉันปล่อยวางความต้องการควบคุมชีวิตของตัวเองได้",
                "ฉันไม่ได้ยึดติดกับความคิดที่ฉันมีเกี่ยวกับตัวเองมากเกินไป",
                "ฉันรู้สึกว่า ฉันถูกกำหนดด้วยความคิดเกี่ยวกับตัวเองน้อยลงเรื่อย ๆ เมื่อเวลาผ่านไป",
                "เมื่อเวลาผ่านไป ฉันยิ่งรู้สึกถึงความต้องการที่จะยึดมั่นถือมั่นอะไร ๆ น้อยลง",
                "ฉันสามารถสัมผัสถึงเรื่องราวขึ้นๆ ลงๆ ในชีวิตได้โดยไม่ติดอยู่กับเรื่องนั้น",
                "ฉันสามารถสังเกตความคิดทางบวกและทางลบที่ฉันมีเกี่ยวกับตัวเองได้ โดยไม่เข้าไปยุ่งเกี่ยวกับความคิดเหล่านั้น"
            ]

        # Set index in questions list
        self.index = 0
        self.length_of_list = len(self.questions)

        # Display the question
        Label(self, text=" ", font=("Sarabun", 20)).pack()
        self.question_label = Label(self, text="{}. {}".format(self.index + 1, self.questions[self.index]),
                                    font=custom_font)
        self.question_label.pack(anchor='w', padx=20, pady=20)

        Label(self, text="ระดับคะแนนและความหมาย", font=custom_font).pack(padx=50, pady=20)

        # Scale descriptions and values
        scale_text = ["ไม่เห็นด้วยอย่างยิ่ง", "ไม่เห็นด้วย", "ไม่เห็นด้วยนิดหน่อย", "เห็นด้วยปานกลาง",
                      "เห็นด้วยนิดหน่อย", "เห็นด้วย", "เห็นด้วยอย่างยิ่ง"]
        scale_values = [("1", 1), ("2", 2), ("3", 3), ("4", 4), ("5", 5), ("6", 6), ("7", 7)]
        self.var = StringVar()
        self.var.set(0)  # initialize

        # Create a frame for the scale table
        scale_frame = Frame(self, borderwidth=2, relief="ridge")
        scale_frame.pack(pady=10, padx=20)

        # Add descriptions in the first row of the table
        for col, text in enumerate(scale_text):
            label = Label(scale_frame, text=text, font=("Sarabun", 20))
            label.grid(row=0, column=col, padx=10, pady=10, sticky='n')

        # Add radio buttons in the second row of the table with larger font for numbers
        for col, (text, value) in enumerate(scale_values):
            radio = Radiobutton(scale_frame, text=text, variable=self.var, value=value, font=("Sarabun", 18))
            radio.grid(row=1, column=col, padx=10, pady=10)

        # Create next question button
        enter_button = ttk.Button(self, text="คำถามถัดไป", command=self.nextQuestion)
        enter_button.pack(ipady=5, pady=20)

    def nextQuestion(self):
        '''
        When button is clicked, add user's input to a list
        and display next question.
        '''
        answer = self.var.get()

        if answer == '0':
            dialogBox("ยังไม่ได้ตอบคำถาม",
                      "โปรดตอบคำถาม.\nและลองใหม่อีกครั้ง")
        elif self.index == (self.length_of_list - 1):
            # get the last answer from user
            selected_answer = self.var.get()

            NonAttachmentToSelf_list.append(selected_answer)
            print("NonAttachmentToSelf", NonAttachmentToSelf_list)

            # Disable interactive widgets before showing the dialog
            for widget in self.winfo_children():
                try:
                    widget.configure(state='disabled')
                except TclError:
                    pass  # Ignore widgets that don't have a state option

            next_survey_text = "จบแบบวัดความไม่ยึดติดตัวตน \n \n \n กด เริ่ม เพื่อเริ่มทำแบบวัด Perceived Stress"
            nextSurveyDialog("แบบสอบถามถัดไป", next_survey_text, lambda: self.controller.show_frame(PerceivedStress))
        else:
            self.index = (self.index + 1) % self.length_of_list

            self.question_label.config(text="{}. {}".format(self.index + 1, self.questions[self.index]))
            selected_answer = self.var.get()
            NonAttachmentToSelf_list.append(selected_answer)

            self.var.set(0)  # reset value for next question
            time.sleep(.2)  # delay between questions

class PerceivedStress(Frame):
    """
    Class that displays the window for the future consumption trends survey questions.
    When the user answers a question, the answer is written to a
    csv file.
    """

    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller

        global PerceivedStress_list

        # Create header label
        ttk.Label(self, text=(
            "ข้อคำถามต่อไปนี้เป็นคำถามเกี่ยวกับความรู้สึกและความคิดของท่านในช่วง 1 เดือนที่ผ่านมา \n"
            "โดยข้อคำถามจะมีความคล้ายคลึงกันและเป็นข้อคำถามในลักษณะที่เกี่ยวกับความบ่อยครั้งเพียงใด \n"
            "ที่ท่านรู้สึกหรือคิดอย่างนั้น แต่อย่างไรก็ตามก็มีความแตกต่างกันในระหว่างข้อคำถามเหล่านั้น \n \n"
            "ซึ่งวิธีที่ดีเพื่อช่วยในการตอบคำถามคือ ท่านควรตอบคำถามแต่ละข้อแยกจากกัน \n"
            "และตอบอย่างรวดเร็ว พยายามอย่านับว่ากี่ครั้งที่ท่านคิดอย่างนั้นแต่ให้เลือกตอบด้วยการคาดคะเนอย่างสมเหตุสมผล\n"),
        borderwidth=2, relief="ridge").pack(padx=10, pady=10)
        # Label(self, text=" ", font=("Sarabun", 20)).pack(pady=10)

        Label(self, text="**หมายเหตุ หลังจากกดเพื่อทำคำถามถัดไป ท่านไม่สามารถกลับมาแก้ไขคำตอบได้**",
              font=custom_font).pack(padx=50, pady=20)

        self.questions = [
            "ในช่วง 1 เดือนที่ผ่านมา บ่อยครั้งเพียงใดที่ท่านรู้สึกผิดหวังหรือไม่สบายใจ เพราะมีบางสิ่งบางอย่างเกิดขึ้นอย่างไม่คาดคิด",
            "ในช่วง 1 เดือนที่ผ่านมา บ่อยครั้งเพียงใดที่มีเหตุการณ์สำคัญที่ท่านไม่สามารถเปลี่ยนแปลงหรือจัดการได้",
            "ในช่วง 1 เดือนที่ผ่านมา บ่อยครั้งเพียงใดที่ท่านรู้สึกเครียดและกระวนกระวายใจ",
            "ในช่วง 1 เดือนที่ผ่านมา บ่อยครั้งเพียงใดที่ท่านรู้สึกว่าท่านสามารถแก้ไขปัญหาที่ทำให้ท่านไม่สบายใจในชีวิตประจำวันได้สำเร็จ",
            "ในช่วง 1 เดือนที่ผ่านมา บ่อยครั้งเพียงใดที่ท่านรู้สึกว่าท่านสามารถจัดการกับปัญหาที่สำคัญในชีวิตได้สำเร็จ",
            "ในช่วง 1 เดือนที่ผ่านมา บ่อยครั้งเพียงใดที่ท่านรู้สึกมั่นใจว่าท่านสามารถแก้ไขหรือจัดการปัญหาได้",
            "ในช่วง 1 เดือนที่ผ่านมา บ่อยครั้งเพียงใดที่ท่านรู้สึกว่าเหตุการณ์ต่าง ๆ ที่เกิดขึ้นเป็นไปตามที่ท่านต้องการให้เป็นไป",
            "ในช่วง 1 เดือนที่ผ่านมา บ่อยครั้งเพียงใดที่ท่านพบว่าตนเองไม่สามารถทำงานได้ทันเวลา",
            "ในช่วง 1 เดือนที่ผ่านมา บ่อยครั้งเพียงใดที่ท่านรู้สึกว่าท่านสามารถกำจัดหรือลดความไม่สบายใจที่เกิดขึ้นได้",
            "ในช่วง 1 เดือนที่ผ่านมา บ่อยครั้งเพียงใดที่ท่านรู้สึกว่าท่านสามารถเอาชนะปัญหาหรืออุปสรรคที่เกิดขึ้นได้",
            "ในช่วง 1 เดือนที่ผ่านมา บ่อยครั้งเพียงใดที่ท่านรู้สึกโกรธหรือไม่พอใจที่ตนเองไม่สามารถจัดการกับเหตุการณ์บางอย่างที่เกิดขึ้นได้",
            "ในช่วง 1 เดือนที่ผ่านมา บ่อยครั้งเพียงใดที่ท่านหมกมุ่นครุ่นคิดอยู่กับเรื่องใดเรื่องหนึ่งเพียงอย่างเดียว",
            "ในช่วง 1 เดือนที่ผ่านมา บ่อยครั้งเพียงใดที่ท่านสามารถตัดสินใจได้ว่าช่วงเวลาใดท่านสามารถจะทำอะไรได้ด้วยตนเอง",
            "ในช่วง 1 เดือนที่ผ่านมา บ่อยครั้งเพียงใดที่ท่านรู้สึกเป็นทุกข์ เนื่องจากปริมาณงานต่าง ๆ มีมากจนท่านไม่สามารถจัดการได้หมด"
        ]

        # Set index in questions list
        self.index = 0
        self.length_of_list = len(self.questions)

        # Display the question on a single line
        Label(self, text=" ", font=("Sarabun", 20)).pack()

        self.question_label = Label(
            self,
            text="{}. {}".format(self.index + 1, self.questions[self.index]),
            font=("Sarabun", 20),  # Use Sarabun font for Thai compatibility
            anchor="w"  # Align text to the left
        )
        self.question_label.pack(anchor='w', padx=20, pady=20)

        Label(self, text="ระดับคะแนนและความหมาย", font=custom_font).pack(padx=50, pady=20)

        # Scale descriptions and values
        scale_text = ["ไม่เคยเลย", "เกือบจะไม่เคย", "บางครั้ง", "บ่อยๆ", "บ่อยมาก"]
        scale_values = [("1", 1), ("2", 2), ("3", 3), ("4", 4), ("5", 5)]
        self.var = StringVar()
        self.var.set(0)  # initialize

        # Create a frame for the scale table
        scale_frame = Frame(self, borderwidth=2, relief="ridge")
        scale_frame.pack(pady=10, padx=20)

        # Add descriptions in the first row of the table
        for col, text in enumerate(scale_text):
            label = Label(scale_frame, text=text, font=("Sarabun", 20))
            label.grid(row=0, column=col, padx=10, pady=10, sticky='n')

        # Add radio buttons in the second row of the table with larger font for numbers
        for col, (text, value) in enumerate(scale_values):
            radio = Radiobutton(scale_frame, text=text, variable=self.var, value=value, font=("Sarabun", 18))
            radio.grid(row=1, column=col, padx=10, pady=10)

        # Create next question button
        enter_button = ttk.Button(self, text="คำถามถัดไป", command=self.nextQuestion)
        enter_button.pack(ipady=5, pady=20)


    def nextQuestion(self):
        '''
        When button is clicked, add user's input to a list
        and display next question.
        '''
        answer = self.var.get()

        if answer == '0':
            dialogBox("ยังไม่ได้ตอบคำถาม",
                      "โปรดตอบคำถาม\nและลองใหม่อีกครั้ง")
        elif self.index == (self.length_of_list - 1):
            # get the last answer from user
            selected_answer = self.var.get()

            PerceivedStress_list.append(selected_answer)
            print("PerceivedStress", PerceivedStress_list)

            # Disable interactive widgets before showing the dialog
            for widget in self.winfo_children():
                try:
                    widget.configure(state='disabled')
                except TclError:
                    pass  # Ignore widgets that don't have a state option

            next_survey_text = "จบแบบวัดการรับรู้ความเครียด  \n \n \n กด เริ่ม เพื่อเริ่มทำแบบวัด Overall Emotional Well being"
            nextSurveyDialog("แบบสอบถามถัดไป", next_survey_text, lambda: self.controller.show_frame(OverallEmotionalWellbeing))
        else:
            self.index = (self.index + 1) % self.length_of_list

            self.question_label.config(text="{}. {}".format(self.index + 1, self.questions[self.index]))
            selected_answer = self.var.get()
            PerceivedStress_list.append(selected_answer)

            self.var.set(0)  # reset value for next question
            time.sleep(.2)  # delay between questions


class OverallEmotionalWellbeing(Frame):
    """
    Class that displays the window for the future consumption trends survey questions.
    When the user answers a question, the answer is written to a
    csv file.
    """

    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller

        global OverallEmotionalWellbeing_list

        # Create header label
        ttk.Label(self, text=(
            "โปรดอ่านข้อความ แล้วเลือกตัวเลขที่ตรงกับความเป็นจริงของท่านที่สุด"),
        borderwidth=2, relief="ridge").pack(padx=10, pady=10)
        Label(self, text=" ", font=("Sarabun", 20)).pack(pady=10)

        self.questions = [
                "ชีวิตทำให้ฉันรู้สึกตื่นเต้น",
                "ฉันรู้สึกสงบสุขในชีวิต",
                "ชีวิตของฉันทำให้ฉันรู้สึกเศร้า",
                "ฉันรู้สึกวิตกกังวลกับชีวิตของฉัน",
                "ฉันรู้สึกพอใจกับชีวิต",
                "ฉันยอมรับชีวิตได้ในแบบที่เป็น",
                "ฉันได้รับความสุขในชีวิต",
                "ฉันรู้สึกไม่พอใจกับชีวิตของฉัน",
                "ฉันรู้สึกเจ็บปวดกับชีวิตของฉัน",
                "ฉันรู้สึกหวาดกลัวกับชีวิตของฉัน",
                "ฉันชื่นชมยินดีกับชีวิตของฉัน",
                "ฉันรู้สึกหดหู่กับชีวิตของฉัน",
                "ฉันรู้สึกว่ากำลังเสียเวลาในชีวิต",
                "ฉันได้รับความพึงพอใจในชีวิต"
            ]

        # Set index in questions list
        self.index = 0
        self.length_of_list = len(self.questions)

        # Display the question
        Label(self, text=" ", font=("Sarabun", 20)).pack()
        self.question_label = Label(self, text="{}. {}".format(self.index + 1, self.questions[self.index]),
                                    font=custom_font)
        self.question_label.pack(anchor='w', padx=20, pady=20)

        Label(self, text="ระดับคะแนนและความหมาย", font=custom_font).pack(padx=50, pady=20)

        # Scale descriptions and values
        scale_text = ["น้อยมากหรือไม่เลย", "น้อย", "ปานกลาง", "มาก", "มากอย่างยิ่ง"]
        scale_values = [("1", 1), ("2", 2), ("3", 3), ("4", 4), ("5", 5)]
        self.var = StringVar()
        self.var.set(0)  # initialize

        # Create a frame for the scale table
        scale_frame = Frame(self, borderwidth=2, relief="ridge")
        scale_frame.pack(pady=10, padx=20)

        # Add descriptions in the first row of the table
        for col, text in enumerate(scale_text):
            label = Label(scale_frame, text=text, font=("Sarabun", 20))
            label.grid(row=0, column=col, padx=10, pady=10, sticky='n')

        # Add radio buttons in the second row of the table with larger font for numbers
        for col, (text, value) in enumerate(scale_values):
            radio = Radiobutton(scale_frame, text=text, variable=self.var, value=value, font=("Sarabun", 18))
            radio.grid(row=1, column=col, padx=10, pady=10)

        self.question_label.pack(anchor='w', padx=20, pady=20)
        Label(self, text="**หมายเหตุ หลังจากกดเพื่อทำคำถามถัดไป ท่านไม่สามารถกลับมาแก้ไขคำตอบได้**",
              font=custom_font).pack(padx=50, pady=20)
        self.question_label.pack(anchor='w', padx=20, pady=20)

        # Create next question button
        enter_button = ttk.Button(self, text="คำถามถัดไป", command=self.nextQuestion)
        enter_button.pack(ipady=5, pady=20)

    def nextQuestion(self):
        """
        When button is clicked, add user's input to a list and display the next question.
        """
        answer = self.var.get()

        if answer == '0':
            dialogBox("ไม่มีคำตอบ", "คุณไม่ได้เลือกคำตอบ.\nลองอีกครั้ง.")
        elif self.index == (self.length_of_list - 1):
            # Add the last answer from the user
            OverallEmotionalWellbeing_list.append(answer)  # Append only once
            print("OverallEmotionalWellbeing", OverallEmotionalWellbeing_list)

            # Save the data once
            self.saveAllAnswers()

            # Show the "Thank you" message
            finished_text = "ขอขอบคุณท่านที่สละเวลาในการตอบแบบประเมิน\n"
            finishedDialog("จบช่วงการตอบแบบประเมิน", finished_text)
        else:
            # Add the selected answer to the list and move to the next question
            OverallEmotionalWellbeing_list.append(answer)  # Append only once
            self.index += 1
            self.question_label.config(text="{}. {}".format(self.index + 1, self.questions[self.index]))
            self.var.set(0)  # Reset value for the next question
            time.sleep(.2)  # Delay between questions

    def saveAllAnswers(self):
        """
        Save all the answers to their respective CSV files.
        """
        filenames = [
            '01_general_answers.csv',
            '02_MAA_answers.csv',
            '03_FFMQ_SF_answers.csv',
            '04_PHLMS_answers.csv',
            '05_RuminativeThinking_answers.csv',
            '06_NonAttachmentToSelf_answers.csv',
            '07_PerceivedStress_answers.csv',
            '08_OverallEmotionalWellbeing_answers.csv'
        ]

        # Include Participant ID and Timestamp in each list
        answers_lists = [
            [status] + [current_datetime] + general_answers_list,
            [status] + [current_datetime] + MAA_list,
            [status] + [current_datetime] + FFMQ_SF_list,
            [status] + [current_datetime] + PHLMS_list,
            [status] + [current_datetime] + RuminativeThinking_list,
            [status] + [current_datetime] + NonAttachmentToSelf_list,
            [status] + [current_datetime] + PerceivedStress_list,
            [status] + [current_datetime] + OverallEmotionalWellbeing_list
        ]

        # Iterate through each filename and corresponding answers list
        for filename, answers in zip(filenames, answers_lists):
            self.writeToFile(filename, answers)

    def writeToFile(self, filename, answer_list):
        """
        Writes the answers to a CSV file.
        Parameters:
            filename (str): The name of the CSV file.
            answer_list (list): The list of answers from the survey section.
        """
        # Create headers dynamically including "Participant ID" and "Timestamp"
        headers = ["Participant ID", "Timestamp"] + ["Q{}".format(i) for i in range(1, len(answer_list) - 2 + 1)]
        file_exists = os.path.isfile(filename)

        # Open the file in append mode
        with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', lineterminator='\n')

            # If the file doesn't exist, write the headers first
            if not file_exists:
                writer.writerow(headers)

            # Ensure no duplicates are written
            if not self.isDuplicateEntry(filename, answer_list):
                writer.writerow(answer_list)

    def isDuplicateEntry(self, filename, answer_list):
        """
        Checks if the current answer_list already exists in the file.
        Parameters:
            filename (str): The name of the CSV file.
            answer_list (list): The list of answers to check.
        Returns:
            bool: True if duplicate, False otherwise.
        """
        if not os.path.exists(filename):
            return False

        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row == answer_list:
                    return True
        return False


class Mockup(Tk):
    def __init__(self,timestamp,update_status):
        Tk.__init__(self)
        print(update_status,timestamp)

# Run program
if __name__ == "__main__":
    app = Survey()
    app.mainloop()