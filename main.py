from cryptography.fernet import Fernet

class PasswordManager:
    
    
    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}
        
        
    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open (path, "wb") as f:
            f.write(self.key)
            
    def load_key(self, path):
        with open (path, "rb") as f:
            self.key = f.read()
            
    def create_password_file(self, path, initual_values = None):
        self.password_file = path
        if initual_values != None:
            for key, value in initual_values.items():
                self.add_password(key, value)
            
    def load_password_file(self, path):
        self.password_file = path
         
        with open(path, "rb") as f:
            for line in f:
                site, encrypted = line.split(":")
                self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()
                
    def add_password(self, site, password):
        self.password_dict[site] = password
        
        if self.password_file is not None:
            with open(self.password_file, "a+") as f:
                 encrypted = Fernet(self.key).encrypt(password.encode())
                 f.write(site + ":" + encrypted.decode() + "\n")
                 
                 
                 
    def get_password(self, site):
        return self.password_dict[site]
    
    
    
    
def main():
    password = {
            "test_site": "test_password"
    }
    
    pm = PasswordManager()
    
    print("""Выберите что нужно сделать:  
(1) Создать новый ключ
(2) Загрузить существующий ключ
(3) Создать новый файл паролей
(4) Загрузить существующий файл паролей
(5) Добавить новый пароль
(6) Получить пароль
(q or 0) Выйти
            
            """)
    
    done = False
    
    while not done:
        choice = input("Выберите действие из списка: ")
        if choice == "1":
            path = input("Введите путь до файла: ")
            pm.create_key(path)
            
        elif choice == "2":
            path = input("Введите путь до файла: ")
            pm.load_key(path)
            
        elif choice == "3":
            path = input("Введите путь до файла: ")
            pm.create_password_file(path, password)
            
        elif choice == "4":
            path = input("Введите путь до файла: ")
            pm.load_password_file(path)
            
        elif choice == "5":
            site = input("Введите название сайта: ")
            password = input("Введите пароль: ")
            pm.add_password(site, password)
            
        elif choice == "6":
            site = input("Введите название сайта: ")
            print(f'Пароль для сайта {site} – {pm.get_password(site)}')
        
        elif choice == "0" or choice == "q":
            done = True
            
        else:
            print("Не понял :/")
        

            

        
    
if __name__ == "__main__":
    main()