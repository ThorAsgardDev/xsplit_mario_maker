
import sys
import os
import time
import configparser
import sheets_api
import tkinter
import tkinter.ttk
import tkinter.filedialog
import tkinter.messagebox
import PIL.Image
import PIL.ImageTk
import itertools
import keyboard


class MainFrame(tkinter.Frame):
	TOKENS_FILENAME = "tokens.ini"

	def __init__(self, window, **kwargs):
		tkinter.Frame.__init__(self, window, **kwargs)
		
		self.window = window
		self.timer_id = None
		
		self.config = configparser.ConfigParser()
		self.config.read("config.ini")
		
		self.contest_lines = None
		self.selected_contest_line_id = None
		
		self.pack(expand = tkinter.YES, fill = tkinter.BOTH)
		
		menu_bar = tkinter.Menu(self.window)
		file_menu = tkinter.Menu(menu_bar, tearoff = 0)
		file_menu.add_command(label = "Open", command = self.on_menu_file_open)
		file_menu.add_command(label = "Save", command = self.on_menu_file_save)
		menu_bar.add_cascade(label = "File", menu = file_menu)
		
		self.window.config(menu = menu_bar)
		
		self.frame = tkinter.Frame(self)
		self.frame.pack(side = tkinter.TOP, fill = tkinter.BOTH)
		
		self.frame_logo = tkinter.Frame(self.frame)
		self.frame_logo.pack(side = tkinter.BOTTOM, fill = tkinter.BOTH)
		
		self.frame_level = tkinter.LabelFrame(self.frame, text = "Level")
		self.frame_level.pack(side = tkinter.TOP, fill = tkinter.BOTH, padx = 5, pady = 5)
		
		self.frame_level_labels = tkinter.Frame(self.frame_level)
		self.frame_level_labels.pack(side = tkinter.LEFT, fill = tkinter.BOTH)
		
		self.frame_level_values = tkinter.Frame(self.frame_level)
		self.frame_level_values.pack(side = tkinter.RIGHT, expand = tkinter.YES, fill = tkinter.BOTH)
		
		self.frame_run = tkinter.LabelFrame(self.frame, text = "Run")
		self.frame_run.pack(side = tkinter.TOP, fill = tkinter.BOTH, padx = 5, pady = 5)
		
		self.frame_run_top = tkinter.Frame(self.frame_run)
		self.frame_run_top.pack(side = tkinter.TOP, fill = tkinter.BOTH)
		
		self.frame_run_bottom = tkinter.Frame(self.frame_run)
		self.frame_run_bottom.pack(side = tkinter.BOTTOM, fill = tkinter.BOTH)
		
		self.frame_run_labels = tkinter.Frame(self.frame_run_top)
		self.frame_run_labels.pack(side = tkinter.LEFT, fill = tkinter.BOTH)
		
		self.frame_run_values = tkinter.Frame(self.frame_run_top)
		self.frame_run_values.pack(side = tkinter.RIGHT, expand = tkinter.YES, fill = tkinter.BOTH)
		
		pil_img = PIL.Image.open("resources/mario-maker.png")
		self.img_logo = PIL.ImageTk.PhotoImage(pil_img) # reference to image must be kept to avoid garbage deletion
		canvas = tkinter.Canvas(self.frame_logo, width = self.img_logo.width(), height = self.img_logo.height())
		canvas.create_image((0, 0), anchor = tkinter.NW, image = self.img_logo)
		canvas.pack(side = tkinter.TOP)
		
		label = tkinter.Label(self.frame_level_labels, text = "N° Concours: ")
		label.pack(anchor = tkinter.W, padx = 5, pady = 5)
		self.combo_contests = tkinter.ttk.Combobox(self.frame_level_values, state = "readonly")
		self.combo_contests.pack(padx = 5, pady = 5, fill = tkinter.X)
		self.combo_contests.bind("<<ComboboxSelected>>", self.on_combo_contests_changed)
		
		label = tkinter.Label(self.frame_level_labels, text = "Navigation: ")
		label.pack(anchor = tkinter.W, padx = 5, pady = 5)
		self.frame_level_values_navigate = tkinter.Frame(self.frame_level_values)
		self.frame_level_values_navigate.pack(side = tkinter.TOP, expand = tkinter.YES, fill = tkinter.BOTH)
		self.button_navigate_previous = tkinter.Button(self.frame_level_values_navigate, relief = tkinter.GROOVE, text = "<<", state = tkinter.DISABLED, command = self.on_previous_click)
		self.button_navigate_previous.pack(side = tkinter.LEFT, expand = tkinter.YES, fill = tkinter.X, padx = 5)
		self.button_navigate_next = tkinter.Button(self.frame_level_values_navigate, relief = tkinter.GROOVE, text = ">>", state = tkinter.DISABLED, command = self.on_next_click)
		self.button_navigate_next.pack(side = tkinter.RIGHT, expand = tkinter.YES, fill = tkinter.X, padx = 5)
		
		label = tkinter.Label(self.frame_level_labels, text = "Thème: ")
		label.pack(anchor = tkinter.W, padx = 5, pady = 5)
		self.label_theme = tkinter.Label(self.frame_level_values)
		self.label_theme.pack(anchor = tkinter.W, padx = 5, pady = 5)
		
		label = tkinter.Label(self.frame_level_labels, text = "Viewer: ")
		label.pack(anchor = tkinter.W, padx = 5, pady = 5)
		self.label_viewer = tkinter.Label(self.frame_level_values)
		self.label_viewer.pack(anchor = tkinter.W, padx = 5, pady = 5)
		
		label = tkinter.Label(self.frame_level_labels, text = "Code level: ")
		label.pack(anchor = tkinter.W, padx = 5, pady = 5)
		self.label_level_id = tkinter.Label(self.frame_level_values)
		self.label_level_id.pack(anchor = tkinter.W, padx = 5, pady = 5)
		
		label = tkinter.Label(self.frame_run_labels, text = "Statut: ")
		label.pack(anchor = tkinter.W, padx = 5, pady = 5)
		self.label_status = tkinter.Label(self.frame_run_values)
		self.label_status.pack(anchor = tkinter.W, padx = 5, pady = 5)
		
		label = tkinter.Label(self.frame_run_labels, text = "Vies perdues: ")
		label.pack(anchor = tkinter.W, padx = 5, pady = 5)
		self.label_lost_lives = tkinter.Label(self.frame_run_values)
		self.label_lost_lives.pack(anchor = tkinter.W, padx = 5, pady = 5)
		
		label = tkinter.Label(self.frame_run_labels, text = "Temps: ")
		label.pack(anchor = tkinter.W, padx = 5, pady = 5)
		self.label_time = tkinter.Label(self.frame_run_values)
		self.label_time.pack(anchor = tkinter.W, padx = 5, pady = 5)
		
		self.button_start_pause = tkinter.Button(self.frame_run_bottom, relief = tkinter.GROOVE, text = "Démarrer", command = self.on_start_pause_click)
		self.button_start_pause.pack(fill = tkinter.X, padx = 5, pady = (5, 0))
		
		self.button_reset = tkinter.Button(self.frame_run_bottom, relief = tkinter.GROOVE, text = "Remettre à zéro", command = self.on_reset_click)
		self.button_reset.pack(fill = tkinter.X, padx = 5)
		
		self.button_validate = tkinter.Button(self.frame_run_bottom, relief = tkinter.GROOVE, text = "Valider", command = self.on_validate_click)
		self.button_validate.pack(fill = tkinter.X, padx = 5)
		
		self.button_give_up = tkinter.Button(self.frame_run_bottom, relief = tkinter.GROOVE, text = "Abandonner", command = self.on_give_up_click)
		self.button_give_up.pack(fill = tkinter.X, padx = 5, pady = (0, 5))
		
		keyboard.add_hotkey(self.config["SHEET"]["HOTKEY_LOST_LIVES_MINUS"], lambda: window.after(1, self.on_hotkey_lost_lives_minus))
		keyboard.add_hotkey(self.config["SHEET"]["HOTKEY_LOST_LIVES_PLUS"], lambda: window.after(1, self.on_hotkey_lost_lives_plus))
		
	def get_selected_level_line(self):
		if self.selected_contest_line_id == None:
			return None
		return self.contest_lines[self.selected_contest_line_id]
		
	def get_level_model_value(self, value_label):
		level_line = self.get_selected_level_line()
		
		if level_line == None:
			return None
			
		return self.model[value_label][level_line]
		
	def set_level_model_value(self, value_label, value):
		level_line = self.get_selected_level_line()
		
		if level_line == None:
			return
			
		self.model[value_label][level_line] = value
		
	def set_lost_lives(self, lost_lives):
		self.set_level_model_value("lost_lives", lost_lives)
		self.label_lost_lives.config(text = lost_lives)
		self.write_file("w", "text-files/lost-lives.txt", lost_lives)
		
	def set_status(self, status):
		self.set_level_model_value("status", status)
		self.label_status.config(text = status)
		self.write_file("w", "text-files/status.txt", status)
		
	def set_time(self, time_str):
		self.set_level_model_value("time", time_str)
		self.label_time.config(text = time_str)
		self.write_file("w", "text-files/time.txt", time_str)
		
	def on_hotkey_lost_lives_minus(self):
		value_str = self.get_level_model_value("lost_lives")
		try:
			value = int(value_str)
			if value >= 1:
				value -= 1
				value = str(value)
				self.set_lost_lives(value)
		except:
			pass
			
	def on_hotkey_lost_lives_plus(self):
		value_str = self.get_level_model_value("lost_lives")
		try:
			value = int(value_str)
			if value < 99999 - 1:
				value += 1
				value = str(value)
				self.set_lost_lives(value)
		except:
			pass
			
	def on_previous_click(self):
		if self.selected_contest_line_id >= 1:
			# if run in progress, save it
			if self.timer_id:
				self.pause_run()
				self.save_level_to_sheet()
			self.selected_contest_line_id -= 1
			self.process_on_selected_level_changed()
			
	def on_next_click(self):
		if self.selected_contest_line_id < len(self.contest_lines) - 1:
			# if run in progress, save it
			if self.timer_id:
				self.pause_run()
				self.save_level_to_sheet()
			self.selected_contest_line_id += 1
			self.process_on_selected_level_changed()
			
	def on_menu_file_open(self):
		file_name = tkinter.filedialog.askopenfilename(defaultextension = "*.rcx", filetypes = [("Mario-maker context files", "*.mcx")])
		if len(file_name) >= 1:
			self.load_context(file_name)
			
	def on_menu_file_save(self):
		file_name = tkinter.filedialog.asksaveasfilename(defaultextension = "*.rcx", filetypes = [("Mario-maker context files", "*.mcx")])
		if len(file_name) >= 1:
			self.save_context(file_name)
			
	def start_timer(self):
		if self.timer_id:
			self.window.after_cancel(self.timer_id)
		self.timer_id = self.window.after(1000, self.update_timer)
		
	def stop_timer(self):
		if self.timer_id:
			self.window.after_cancel(self.timer_id)
			self.timer_id = None
			
	def start_run(self):
		self.button_start_pause.config(text = "Pause")
		if self.combo_contests.current() >= 0:
			self.write_file("w", "text-files/contest-number.txt", self.combo_contests.cget("values")[self.combo_contests.current()])
			self.write_file("w", "text-files/theme.txt", self.label_theme.cget("text"))
			self.write_file("w", "text-files/viewer.txt", self.label_viewer.cget("text"))
			self.write_file("w", "text-files/level-id.txt", self.label_level_id.cget("text"))
			self.write_file("w", "text-files/status.txt", self.label_status.cget("text"))
			self.write_file("w", "text-files/lost-lives.txt", self.label_lost_lives.cget("text"))
			self.write_file("w", "text-files/time.txt", self.label_time.cget("text"))
			
		self.start_timer()
		
	def pause_run(self):
		self.button_start_pause.config(text = "Démarrer")
		self.stop_timer()
		
	def on_start_pause_click(self):
		if self.button_start_pause.cget("text") == "Démarrer":
			self.start_run()
		else:
			self.pause_run()
			self.save_level_to_sheet()
			
	def on_reset_click(self):
		self.pause_run()
		self.set_time("00:00:00")
		self.set_status("A faire")
		self.set_lost_lives("0")
		self.save_level_to_sheet()
		
	def on_validate_click(self):
		self.set_status("Validé")
		self.pause_run()
		self.save_level_to_sheet()
		
	def on_give_up_click(self):
		self.set_status("Abandonné")
		self.pause_run()
		self.save_level_to_sheet()
		
	def timeStrToSec(self, t):
		if t == "":
			t = "00:00:00"
			
		v = t.split(":")
		
		if len(v) >= 3:
			val = int(v[0]) * 3600 + int(v[1]) * 60 + int(v[2])
		elif len(v) >= 2:
			val = int(v[0]) * 60 + int(v[1])
		else:
			val = int(v[0])
			
		return val
		
	def timeSecToStr(self, t):
		h = str(t // 3600)
		if len(h) < 2:
			h = "0" + h
		m = ("0" + str((t % 3600) // 60))[-2:]
		s = ("0" + str(t % 60))[-2:]
		return h + ":" + m + ":" + s
		
	def update_timer(self):
		time_str = self.get_level_model_value("time")
		t = self.timeStrToSec(time_str)
		t += 1
		self.set_time(self.timeSecToStr(t));
		self.timer_id = self.window.after(1000, self.update_timer)
		
	def on_combo_contests_changed(self, event):
		self.process_on_combo_contests_changed()
		
	def process_on_combo_contests_changed(self):
		self.contest_lines = self.create_contest_lines(self.get_combo_value(self.combo_contests))
		self.selected_contest_line_id = 0
		self.process_on_selected_level_changed()
		
	def create_contest_lines(self, contest_number_value):
		lines = []
		i = 0
		for contest_number in self.model["contest_number"]:
			if contest_number == contest_number_value:
				lines.append(i)
			i += 1
			
		return lines
		
	def update_navigate_buttons_status(self):
		button_previous_target_state = tkinter.NORMAL
		button_next_target_state = tkinter.NORMAL
		if len(self.contest_lines) == 0:
			button_previous_target_state = tkinter.DISABLED
			button_next_target_state = tkinter.DISABLED
		else:
			if self.selected_contest_line_id < 1:
				button_previous_target_state = tkinter.DISABLED
				
			if self.selected_contest_line_id >= len(self.contest_lines) - 1:
				button_next_target_state = tkinter.DISABLED
				
		self.button_navigate_previous.config(state = button_previous_target_state)
		self.button_navigate_next.config(state = button_next_target_state)
		
	def process_on_selected_level_changed(self):
		self.pause_run()
		self.update_navigate_buttons_status()
		self.label_theme.config(text = self.get_level_model_value("theme"))
		self.label_viewer.config(text = self.get_level_model_value("viewer"))
		self.label_level_id.config(text = self.get_level_model_value("level_id"))
		self.label_status.config(text = self.get_level_model_value("status"))
		self.label_time.config(text = self.get_level_model_value("time"))
		self.label_lost_lives.config(text = self.get_level_model_value("lost_lives"))
		
	def fill_contests(self):
		lst = self.model["contest_number"]
		self.combo_contests.config(values = sorted(set(lst), key=lst.index))
		
		if len(lst) >= 1:
			self.combo_contests.current(0)
			return True
			
		return False
		
	def write_file(self, mode, file_name, value):
		nb_retries = 0
		while nb_retries < 5:
			try:
				with open(file_name, mode) as f:
					f.write(value)
				break
			except:
				nb_retries += 1
				time.sleep(0.01)
				
	def get_combo_value(self, combo):
		value = ""
		current_index = combo.current()
		values = combo.cget("values")
		if current_index >= 0 and current_index < len(values):
			value = values[current_index]
		return value
		
	def select_combo_value(self, combo, value):
		values = combo.cget("values")
		
		i = 0
		for v in values:
			if v == value:
				combo.current(i)
				return True
			i += 1
			
		return False
		
	def build_model(self, values):
		keys = [
			{"label": "theme", "default_value": ""},
			{"label": "contest_number", "default_value": ""},
			{"label": "viewer", "default_value": ""},
			{"label": "level_id", "default_value": ""},
			{"label": "status", "default_value": "A faire"},
			{"label": "time", "default_value": "00:00:00"},
			{"label": "lost_lives", "default_value": "0"},
		]
		
		model = {}
		for key in keys:
			model[key["label"]] = []
		
		if values:
			current_column = 0
			ranges = values["valueRanges"]
			
			max_nb_lines = 0
			for range in ranges:
				nb_lines = 0
				if "values" in range:
					values = range["values"]
					for value in values:
						nb_lines += 1
						if len(value) < 1:
							model[keys[current_column]["label"]].append(keys[current_column]["default_value"])
						else:
							model[keys[current_column]["label"]].append(value[0])
							
					if max_nb_lines < nb_lines:
						max_nb_lines = nb_lines
						
				current_column += 1
				
			for key in keys:
				model[key["label"]].extend(list(itertools.repeat(key["default_value"], max_nb_lines - len(model[key["label"]]))))
				
		return model
		
	def load_sheet(self):
		config_sheet = self.config["SHEET"]
		sheet_name = config_sheet["SHEET_NAME"]
		first_line = config_sheet["FIRST_LINE"]
		ranges = [
			sheet_name + "!" + config_sheet["THEME_COLUMN"] + first_line + ":" + config_sheet["THEME_COLUMN"],
			sheet_name + "!" + config_sheet["CONTEST_NUMBER_COLUMN"] + first_line + ":" + config_sheet["CONTEST_NUMBER_COLUMN"],
			sheet_name + "!" + config_sheet["VIEWER_COLUMN"] + first_line + ":" + config_sheet["VIEWER_COLUMN"],
			sheet_name + "!" + config_sheet["LEVEL_ID_COLUMN"] + first_line + ":" + config_sheet["LEVEL_ID_COLUMN"],
			sheet_name + "!" + config_sheet["STATUS_COLUMN"] + first_line + ":" + config_sheet["STATUS_COLUMN"],
			sheet_name + "!" + config_sheet["TIME_COLUMN"] + first_line + ":" + config_sheet["TIME_COLUMN"],
			sheet_name + "!" + config_sheet["LOST_LIVES_COLUMN"] + first_line + ":" + config_sheet["LOST_LIVES_COLUMN"],
		]

		values = self.sheets_api.get_values(ranges)
		
		self.model = self.build_model(values)
		
	def save_level_to_sheet(self):
		config_sheet = self.config["SHEET"]
		sheet_name = config_sheet["SHEET_NAME"]
		first_line = config_sheet["FIRST_LINE"]
		level_line = self.get_selected_level_line()
		line = str(int(first_line) + level_line)
		ranges_values = [
			{
				"range": sheet_name + "!" + config_sheet["STATUS_COLUMN"] + line + ":" + config_sheet["STATUS_COLUMN"] + line,
				"values": [[self.get_level_model_value("status")]]
			},
			{
				"range": sheet_name + "!" + config_sheet["TIME_COLUMN"] + line + ":" + config_sheet["TIME_COLUMN"] + line,
				"values": [[self.get_level_model_value("time")]]
			},
			{
				"range": sheet_name + "!" + config_sheet["LOST_LIVES_COLUMN"] + line + ":" + config_sheet["LOST_LIVES_COLUMN"] + line,
				"values": [[self.get_level_model_value("lost_lives")]]
			},
		]
		
		self.sheets_api.set_values(ranges_values)
		
	def load(self):
		if not os.path.isfile(MainFrame.TOKENS_FILENAME):
			tkinter.messagebox.showerror("Error", " File "+ MainFrame.TOKENS_FILENAME +" not found. Please run grant_permissions.bat.")
			sys.exit()
			
		self.sheets_api = sheets_api.SheetsApi(self.config["SHEET"]["GDOC_API_KEY"], self.config["SHEET"]["OAUTH_CLIENT_ID"], self.config["SHEET"]["OAUTH_CLIENT_SECRET"], self.config["SHEET"]["SPREAD_SHEET_ID"], MainFrame.TOKENS_FILENAME)
		self.load_sheet()
		if self.fill_contests():
			self.load_context("context.sav")
			self.process_on_combo_contests_changed()
		
	def load_context(self, file_name):
		if os.path.exists(file_name):
			config = configparser.ConfigParser()
			config.read(file_name)
			self.select_combo_value(self.combo_contests, config["CONTEXT"]["contest_number"])
			
	def save_context(self, file_name):
		config = configparser.ConfigParser()
		
		config["CONTEXT"] = {
			"contest_number": self.get_combo_value(self.combo_contests),
		}
		
		with open(file_name, "w") as f:
			config.write(f)
		
	def on_close(self):
		self.save_context("context.sav")
		try:
			self.window.destroy()
		except:
			pass
			
def main():
	window = tkinter.Tk()
	window.title("Mario Maker")
	window.geometry("300x600")
	window.geometry(("+" + str(int((window.winfo_screenwidth() - 300) / 2)) + "+"+ str(int((window.winfo_screenheight() - 600) / 2))))
	f = MainFrame(window)
	window.protocol("WM_DELETE_WINDOW", f.on_close)
	icon = tkinter.PhotoImage(file = "resources/icon.png")
	window.tk.call("wm", "iconphoto", window._w, icon)
	window.after(1, f.load)
	window.mainloop()
	
if __name__ == "__main__":
	main()
	