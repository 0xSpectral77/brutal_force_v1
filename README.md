# 🔐 Brutal-Force

**Brutal-Force** es una herramienta escrita en **Python 3** diseñada para realizar **ataques de fuerza bruta controlados** contra usuarios locales de sistemas Linux, **exclusivamente en entornos autorizados**, como **CTFs**, **laboratorios** o **máquinas de pruebas**.

> ⚠️ **Uso estrictamente educativo y ético**

---

## 📌 Características

- Ataque de fuerza bruta contra usuarios locales Linux  
- Uso de diccionarios personalizados  
- Barra de progreso en tiempo real  
- Manejo de interrupciones (`Ctrl + C`)  
- Salida clara con colores ANSI  
- Pensada para **CTFs y laboratorios de pentesting**

---

## 🛠️ Requisitos

- Python **3.7+**
- Sistema operativo **Linux**
- Permisos para ejecutar `su`
- Diccionario de contraseñas

---

## 🚀 Instalación

Clona el repositorio:

```bash
git clone https://github.com/tu-usuario/brutal-force.git
cd brutal-force


Otorga permisos de ejecución:

chmod +x brutal-force.py
---

## 📖 Uso

./brutal-force.py -u <usuario> -w <wordlist>
