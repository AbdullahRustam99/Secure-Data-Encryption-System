import streamlit as st
import hashlib
from cryptography.fernet import Fernet 

if 'KEY' not in st.session_state:
    st.session_state.KEY = Fernet.generate_key()
if 'failed_attempts' not in st.session_state:
    st.session_state.failed_attempts = {}
if 'lockout_time' not in st.session_state:
    st.session_state.lockout_time = {}
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
    st.rerun()
if 'data' not in st.session_state:
    st.session_state.data = {}


cipher = Fernet(st.session_state.KEY)

def encrypt_data(text, passkey):
	passkey = hashlib.sha256(passkey.encode()).digest()
	encrypted_text = cipher.encrypt(text.encode())
	st.session_state["data"][st.session_state.current_user]["encrypted_text"] = encrypted_text.decode()
	st.session_state["data"][st.session_state.current_user]["passkey"] = passkey


def decrypt_data(text,passkey):
	passkey = hashlib.sha256(passkey.encode()).digest()
	if passkey == st.session_state.data[st.session_state.current_user]["passkey"]:
		decrypted_text = cipher.decrypt(text.encode()).decode()
		return decrypted_text
	else:
		st.session_state.failed_attempts[st.session_state.current_user] = st.session_state.failed_attempts.get(st.session_state.current_user, 0) + 1


st.title("Secure Data Encryption System")

if not st.session_state.current_user:

	option = st.radio("Option : ",("Register","Login",))

	if option == "Register":

		userName = st.text_input("Enter Your Full Name : ")
		password = st.text_input("Enter Password : ", type="password")

		if userName == "" or password == "":
			st.warning("Please Enter Your Name and Password")
		else:
			if st.button("Register"):
				if userName in st.session_state.data:
					st.error("User Already Exist")
				else:	
					st.session_state.data[userName] = {
						"username": userName,
						"password": password,
						"encrypted_text": "",
						"passkey": ""
					}
					st.success("Registration Successful")
					st.session_state.current_user = userName

	elif option == "Login":

		userName = st.text_input("Enter Your  UserName : ")
		password = st.text_input("Enter Password : ", type="password")	

		if userName == "" or password == "":
			st.warning("Please Enter Your UserName and Password")
		else:
			if st.button("login"):
				if userName not in st.session_state.data:
					st.error("User Not Found")
				else:	
					if userName == st.session_state.data[userName]["username"] and password == st.session_state.data[userName]["password"]:
						st.success("Login Successful")
						st.session_state.current_user = userName
					else:
						st.error("Incorrect Username or Password")

else:
	st.markdown(f"<p class=text> Welcome : {st.session_state.current_user}</p>", unsafe_allow_html=True)
	option = st.radio("Option",("Secure Data","Retrive Data","Logout"))

	if option == "Secure Data":
		encrypt_text = st.text_area("Enter Any Thing To Secure : ")
		passkey = st.text_input("Enter Passkey : ")

		if encrypt_text == "" or passkey == "":
			st.warning("Please Enter Your Text and Passkey")
		else:
			if st.button("Secure Data"):
				encrypt_data(encrypt_text,passkey)
				st.success("Data Encrypted Successfully")

	if option == "Retrive Data":
		passkey = st.text_input("Enter Passkey : ")

		if passkey == "":
			st.warning("Please Enter Your Passkey")
		else:
			if st.button("Retrive Data"):
					
					decrypt_text = st.session_state.data[st.session_state.current_user]["encrypted_text"]
					decrypt_text = decrypt_data(decrypt_text,passkey)

					if decrypt_text:
						st.write("Decrypted Text : ", decrypt_text)
						st.success("Data Retrived Successfully")
					else:
						st.error("Incorrect Passkey")	
						attempt = st.session_state.failed_attempts.get(st.session_state.current_user, 0)
						st.warning(f"Failed Attempts: {attempt}")
						if attempt >= 3:
							st.session_state.failed_attempts[st.session_state.current_user] = 0

							st.session_state.current_user = None
							st.error("Too many failed attempts. Loging Out.....!")
							
	if option == "Logout":
		if st.button("Logout"):
			st.session_state.current_user = None
			st.success("Logout Successfully")


st.markdown("""
<style>
	#secure-data-encryption-system{
	    background-image: linear-gradient(to right top, #00d0b4, #43df9b, #7eeb76, #bcf34a, #fff400);
	    color:#d72638;
	    padding: 20px;
	    border-radius: 10px;
	    box-shadow: 0 4px 8px rgba(225, 225, 225, .7);
	    font-family: 'Arial', sans-serif;
	    text-align: center;
	    text-shadow: 2px 2px 4px rgba(0, 0, 0, 1);
	    margin: 20px auto;
	    border: .7px solid #000;
	    }    

	    .stRadio{
	    display: flex;
	    gap: 20px;
	    text-align: center;
	    font-family: 'Arial', sans-serif;

	    }

	    .st-b3 {
             display: flex;
	     flex-direction: row;
             align-content: center;
	    font-family: 'Arial', sans-serif;
	    
	    }
	    
	    .st-emotion-cache-165fv6u {
	    text-align: center;
	    font-size: 20px;
	    font-family: 'Arial', sans-serif;
	    }

	    .text {
	    text-align: center;
	    font-size: 45px;
	    text-transform: uppercase;
	    border-radius: 10px;
	    color: #fff;
	    padding: 10px;
	    margin:10px 0;
	    box-shadow: 0 4px 8px rgba(225, 225, 225, .3);
	    font-family: 'Arial', sans-serif;
	    font-weight: bold;

	    }

	   
	    
</style>
	    """,unsafe_allow_html=True)

