import tkinter as tk
from tkinter import messagebox
import requests

def send_message():
    url = url_entry.get().strip()
    normal_text = message_entry.get("1.0", tk.END).strip()
    embed_text = embed_entry.get("1.0", tk.END).strip()
    image_url = image_url_entry.get().strip()
    mode = mode_var.get()

    if not url:
        messagebox.showwarning("入力エラー", "Webhook URLを入力してください。")
        return

    data = {}

    #
    if mode in ("normal", "both"):
        if normal_text:
            data["content"] = normal_text

    
    if mode in ("embed", "both"):
        if embed_text:
            embed = {
                "description": embed_text
            }
            if image_url:
                embed["image"] = {"url": image_url}
            data.setdefault("embeds", []).append(embed)
        else:
            if mode == "embed":
                messagebox.showwarning("入力エラー", "埋め込み本文を入力してください。")
                return

    if not data:
        messagebox.showwarning("入力エラー", "送信する内容がありません。")
        return

    try:
        response = requests.post(url, json=data)
        if response.status_code in (200, 204):
            messagebox.showinfo("成功", "メッセージを送信しました！")
            message_entry.delete("1.0", tk.END)
            embed_entry.delete("1.0", tk.END)
            image_url_entry.delete(0, tk.END)
        else:
            messagebox.showerror("エラー", f"送信に失敗しました。ステータスコード: {response.status_code}")
    except Exception as e:
        messagebox.showerror("エラー", f"送信中に例外が発生しました:\n{e}")

# 
root = tk.Tk()
root.title("Discord Webhook 送信ツール")
root.geometry("500x550")

tk.Label(root, text="Webhook URL").pack()
url_entry = tk.Entry(root, width=60)
url_entry.pack(pady=5)


mode_var = tk.StringVar(value="normal")
tk.Label(root, text="送信モードを選択：").pack()
tk.Radiobutton(root, text="通常めっせーじのみ", variable=mode_var, value="normal").pack(anchor="w", padx=20)
tk.Radiobutton(root, text="埋め込みのみ", variable=mode_var, value="embed").pack(anchor="w", padx=20)
tk.Radiobutton(root, text="両方送信", variable=mode_var, value="both").pack(anchor="w", padx=20)


tk.Label(root, text="通常メッセージ").pack()
message_entry = tk.Text(root, height=5, width=60)
message_entry.pack(pady=5)


tk.Label(root, text="埋め込みメッセージ").pack()
embed_entry = tk.Text(root, height=5, width=60)
embed_entry.pack(pady=5)


tk.Label(root, text="埋め込み画像URL（任意）").pack()
image_url_entry = tk.Entry(root, width=60)
image_url_entry.pack(pady=5)


tk.Button(root, text="送信", command=send_message).pack(pady=15)

root.mainloop()
