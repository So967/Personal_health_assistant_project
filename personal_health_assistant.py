import tkinter as tk
from tkinter import messagebox
import requests
import threading


OPENROUTER_API_KEY = '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' 


def get_health_advice():
    symptoms = symptom_input.get("1.0", tk.END).strip()
    if not symptoms:
        messagebox.showwarning("Input Error", "Please enter your symptoms.")
        return

    output_area.config(state='normal')
    output_area.delete("1.0", tk.END)
    output_area.insert(tk.END, "Analyzing symptoms, please wait...\n")
    output_area.config(state='disabled')

    def fetch_advice():
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "openai/gpt-3.5-turbo",
                    "messages": [
                        {"role": "system", "content": "You are a personal health assistant providing health advice based on symptoms."},
                        {"role": "user", "content": f"I am experiencing the following symptoms: {symptoms}. Please provide potential causes, treatments, and when to seek medical help."}
                    ],
                    "temperature": 0.7
                }
            )

            if response.status_code != 200:
                raise Exception("API call failed")

            advice = response.json()['choices'][0]['message']['content']

            output_area.config(state='normal')
            output_area.delete("1.0", tk.END)
            output_area.insert(tk.END, advice)
            output_area.config(state='disabled')

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch health advice.\n{str(e)}")
            output_area.config(state='normal')
            output_area.delete("1.0", tk.END)
            output_area.insert(tk.END, "Error fetching health advice. Please try again later.")
            output_area.config(state='disabled')

    threading.Thread(target=fetch_advice).start()


root = tk.Tk()
root.title("Personal Health Assistant")
root.geometry("700x600")
root.config(bg="#e8f0fe")


title = tk.Label(root, text="Personal Health Assistant", font=("Helvetica", 22, "bold"), bg="#e8f0fe", fg="#1a237e")
title.pack(pady=20)


frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20, relief="ridge", bd=3)
frame.pack(pady=10, padx=30, fill='both', expand=True)


label = tk.Label(frame, text="Enter your symptoms below:", font=("Helvetica", 13, "bold"), bg="white", fg="#1b5e20")
label.pack(anchor="w")


symptom_input = tk.Text(frame, height=6, width=65, font=("Helvetica", 12), wrap=tk.WORD, bd=2, relief="solid")
symptom_input.pack(pady=10)


generate_btn = tk.Button(frame, text="Get Health Advice", font=("Helvetica", 12, "bold"),
                         bg="#1565c0", fg="white", height=2, command=get_health_advice)
generate_btn.pack(pady=10, fill='x')


output_label = tk.Label(frame, text="AI Generated Advice:", font=("Helvetica", 13, "bold"), bg="white", fg="#4e342e")
output_label.pack(anchor="w", pady=(10, 0))


output_area = tk.Text(frame, height=12, width=65, font=("Helvetica", 12), wrap=tk.WORD,
                      state='disabled', bg="#f5f5f5", relief="sunken", bd=2)
output_area.pack(pady=10)


root.mainloop()