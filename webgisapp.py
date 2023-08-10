import streamlit as st
from streamlit_option_menu import option_menu
from App import home, login, peta, register, profile, Upload1, Contact_us, imageprofile, profileadmin
from App.login import login1
from App.register import register1
from App.login import get_session_state
from App.login import logout_user
from PIL import Image, ImageDraw
from App.imageprofile import profile_circle 
from App.Generateiduser import get_id_generate


# import your app modules here



App = [
    {"func": home.app, "title": "Home", "icon": "house"},
    {"func": peta.app, "title": "Map", "icon": "map"},
    {"func": profile.app, "title": "Profile", "icon": "person"},
    {"func": profileadmin.app, "title": "Profile Admin", "icon": "person"},
    {"func": Upload1.app, "title": "Upload","icon": "" },
    {"func": Contact_us.app, "title": "Contact Us","icon": "envelope" }
]

titles = [app["title"] for app in App]
titles_lower = [title.lower() for title in titles]
icons = [app["icon"] for app in App]

params = st.experimental_get_query_params()

if "page" in params:
    default_index = int(titles_lower.index(params["page"][0].lower()))
else:
    default_index = 0

session_state = get_session_state()
id_user = get_id_generate()

# main app
def app():
    if (session_state.login is not None) and (session_state.session_data is not None) and (session_state.session_data['status_user'] == "Admin"):
        menuafterloginadmin()
        print (session_state.login)
        print (session_state.session_data)
        print (id_user.user_id)
        print (id_user.user_data_ewkb)
    
    elif session_state.login is not None and session_state.session_data is not None:
        menuafterloginuser()
        print (session_state.login)
        print (session_state.session_data)
    
    else:
        menubeforelogin()
        print (session_state.login)
        print (session_state.session_data)

# A dictionary of apps in the format of {"App title": "App icon"}
# More icons can be found here: https://icons.getbootstrap.com

# Menu Before Login
def menubeforelogin():
    show_sidebar = True  # Set the condition to show or hide the sidebar
    show_main_menu = True  # Set the condition to show or hide the main menu

    if show_main_menu:
            #Horizontal menu
            selected = option_menu (
                menu_title= None, #required
                options=["Home", "Map", "Contact Us","Login or Register"], #required
                icons=["house", "map", "envelope"], #optional
                # options=["Home", "Map", "Contact", "Login", "Sign Up"], #required
                # icons=["house", "map", "envelope", "person-circle", "person"], #optional
                # menu_icon="cast", #optional
                default_index=0, #optional
                orientation="horizontal",
            )


            for app in App:
                if app["title"] == selected:
                    app["func"]()
                    break


    if show_sidebar:
        #sidebar menu login 
        options2 = ["Login", "Register"]
        choice = st.sidebar.selectbox("Select an option", options2)
        if choice == "Login" and selected == "Login or Register":
            login1() 
            if session_state.login == True:
                st.experimental_rerun()
                        
        elif choice == "Register" and selected == "Login or Register":
            register1()
            
# Menu After login User
def menuafterloginuser():
    show_sidebar = True  # Set the condition to show or hide the sidebar
    show_main_menu = True  # Set the condition to show or hide the main menu

    if show_main_menu:
            #Horizontal menu
            selected = option_menu (
                menu_title= None, #required
                options=["Home", "Map", "Upload","Contact Us","Profile"], #required
                icons=["house", "map","" ,"envelope","person"], #optional
                default_index=0, #optional
                orientation="horizontal",
            )


            for app in App:
                if app["title"] == selected:
                    app["func"]()
                    break


    if show_sidebar:
        #sidebar menu login 
        st.sidebar.write(f"Welcome, user {session_state.session_data['username']}!")
        profile_circle()

            

        if st.sidebar.button("Logout"):
            logout_user()
        if session_state.login == False:
            st.experimental_rerun()  # Rerun the app when the script is executed again


# Menu After login Admin
def menuafterloginadmin():
    show_sidebar = True  # Set the condition to show or hide the sidebar
    show_main_menu = True  # Set the condition to show or hide the main menu

    if show_main_menu:
            #Horizontal menu
            selected = option_menu (
                menu_title= None, #required
                options=["Home", "Map", "Upload","Contact Us","Profile Admin"], #required
                icons=["house", "map","" ,"envelope","person"], #optional
                default_index=0, #optional
                orientation="horizontal",
            )


            for app in App:
                if app["title"] == selected:
                    app["func"]()
                    break


    if show_sidebar:
        #sidebar menu login 
        st.sidebar.write(f"Welcome, user {session_state.session_data['username']}!")
        profile_circle()

        if st.sidebar.button("Logout"):
            logout_user()
        if session_state.login == False:
            st.experimental_rerun()  # Rerun the app when the script is executed again

# Run the app
if __name__ == "__main__":
    app()