import streamlit as st
import sympy as sp
import re  # Import re for regex-based string manipulation

# Define variable for symbol x to be used in mathematical expressions
x = sp.symbols('x')

# Values to test equivalence (checking correctness at these points)
TEST_POINTS = [1,2,3,4,5]

# Function to preprocess user input by ensuring multiplication is implied (like "6x" becoming "6*x")
def preprocess_input(expression):

    # 0. Process inverse trig inputs
    expression = re.sub(r'arc', r'a', expression)

    # 0.1 Absolute value
    expression = re.sub(r'\|([^|]+)\|', r'(abs(\1))', expression)

    # 1. Insert * between number and variable (e.g., 2x → 2*x)
    expression = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expression)

    # 2. Convert sin2x to sin(2*x), cos3x to cos(3*x), etc.
    expression = re.sub(r'(sin|cos|tan|csc|sec|cot|sqrt|cbrt|ln|log)(h?)(\d\*)?([a-zA-Z])', r'\1\2(\3\4)', expression)
    expression = re.sub(r'(sin|cos|tan|csc|sec|cot|sqrt|cbrt|ln|log)(h?)(\d)', r'\1\2(\3)', expression)
    # 3. Insert * between variable and function (e.g., xsinx → x*sin x)
    expression = re.sub(r'(x|\))([a-zA-Z])', r'\1*\2', expression)

    expression = re.sub(r'(\d|\))(\()', r'\1*\2', expression)

    return expression


# Main function to control the flow of the Streamlit app
def main():
    st.title("Integration Techniques")
    
    # Initialize session state variables if not already present
    if "page" not in st.session_state:
        st.session_state.page = "menu"  # Start at the menu page
    if "question_index" not in st.session_state:
        st.session_state.question_index = 0  # Start at the first question
    if "feedback" not in st.session_state:
        st.session_state.feedback = ""  # No feedback at the start
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""  # No user input at the start
    if "answered_correctly" not in st.session_state:
        st.session_state.answered_correctly = False  # Track if the answer is correct

    # Based on the current page, either show the menu or the quiz
    if st.session_state.page == "menu":
        show_menu()
    else:
        show_notes()
        show_quiz()






    
def show_notes():
    if st.session_state.page == "u_sub":
        st.subheader("U-Sub")
        st.markdown("""
        - Technique that can solve most of the complicated integral problems (in Math 21).
        - Used when the integral does not have a direct formula and is already simplified.
        """)
        st.write("U-sub is a powerful technique, but the challenge lies in figuring out which expression to substitute with $u$. We can never be certain that our choice of $u$ is correct, so here are the following tips.")
        
        st.write('')
        st.write("**Good candidates for u-sub:**")
        st.markdown("""
        1. Inside of a parenthesis (Grouped expressions, base of an exponent, etc.)
        2. The denominator or the radicand if there is a radical.
        3. Looking ahead that the resulting $du$ will simplify the integrand (best way and needs practice)
        4. Practice.
        5. The $u$ must be simple. Choose $u$ so that there is no need for the product rule or complicated chain rule when obtaining $du$.
        """)
        st.write("**Note:** When performing u-sub, the resulting integral must have $u$ as the only variable. There should be no $x$ left. If it is not possible to express all terms of $x$ into $u$, then the choose of $u$ in u-sub is incorrect.")
        

        st.write(''); st.write(''); st.write('')
        st.subheader('Example A:')
        st.latex(r"\int \sec^2 x(\sin x+\tan^2 x) \, dx")
        st.write("""
        Before performing u-sub, simplify the integrand first if applicable.
        """)
        st.latex(r"= \int (\sec x \tan x + \sec^2 x \tan^2 x) \, dx")
        st.write("""
        Next, we can see that the first term can be solved right away, while the second term doesn’t have a direct formula and can’t be simplified further. Thus, it will need u-sub to solve.
        """)
        st.latex(r"= \sec x + \int \sec^2 x \tan^2 x \, dx")
        st.write("""
        For u-sub, notice that when $u = \\tan x$, then $du = \\sec² x dx$, which is present on the integral. Thus by look ahead, $u = \\tan x$ is a good u-sub as it simplifies the integral further.
        """)
        st.latex(r"u = \tan x, \quad \, du = \sec^2 x \, dx \, \ \rightarrow \, \ \frac{1}{\sec^2 x} \, du = dx")
        st.write("""
        Hence,
        """)
        st.latex(r"= \sec x + \int \sec^2 x \, u^2 \frac{1}{\sec^2 x} \, du")
        st.latex(r"= \sec x + \int u^2 \, du")
        st.latex(r"= \sec x + \frac{1}{3} u^3 + C")
        st.write("""
        Substitute $x$ back to $u$.
        """)
        st.latex(r"= \boxed{\sec x + \frac{1}{3} \tan^3 x + C}")
        
        st.write(''); st.write(''); st.write('')
        st.subheader('Example B:')
        st.latex(r"\int (4x - 1)^2(2x - 1)^4 \, dx")
        st.write("""
        One way to solve the integral is to expand the whole expression first, but that approach is too difficult and time-consuming. Instead, we can use u-sub and we have the choice to let $u$ as $4x-1$ or $2x-1$. The better option in this case is $u = 2x - 1$ so that we can avoid expanding $(2x - 1)^4$, and squaring an expression is much simpler than raising it to the fourth power.
        """)
        st.latex(r"u = 2x - 1, \quad \, du = 2 \, dx \ \, \rightarrow \, \ \frac{1}{2} du = dx")
        st.write("""
        Thus, the integral becomes:
        """)
        st.latex(r"= \frac{1}{2} \int (4x - 1)^2 u^4 \, du")
        st.write("""
        In the integral, we have the remaining $(4x - 1)^2$ to turn into u before proceeding. To achieve this, we must express $u = 2x - 1$ into $4x - 1$.
        """)
        st.latex(r"u = 2x - 1")
        st.write("""
        We want the coefficient of $x$ to be $4$, so we multiply by 2:
        """)
        st.latex(r"2u = 4x - 2")
        st.write("""
        We want $4x - 1$, so next, we add both sides by 1:
        """)
        st.latex(r"2u + 1 = 4x - 1")
        st.write("""
        Thus, we have:
        """)
        st.latex(r"= \frac{1}{2} \int (2u + 1)^2 u^4 \, du")
        st.write("""
        Now, this is much easier to simplify.
        """)
        st.latex(r"= \frac{1}{2} \int (4u^2 + 4u + 1) u^4 \, du")
        st.latex(r"= \frac{1}{2} \int (4u^6 + 4u^5 + u^4) \, du")
        st.latex(r"= \frac{1}{2} \left( \frac{4}{7} u^7 + \frac{4}{6} u^6 + \frac{1}{5} u^5 \right) + C")
        st.latex(r"= \boxed{\frac{2}{7} (2x - 1)^7 + \frac{1}{3} (2x - 1)^6 + \frac{1}{10} (2x - 1)^5 + C}")

    elif st.session_state.page == "ibp":
        st.subheader("IBP")
        st.write('Integration by parts is the "Product Rule" version of integrals. It follows the rule:')
        st.latex(r"\int u \,dv = uv - \int v \,du")
        st.write("And choosing the expression for $u$ follows the mnemonic **LIATE**.")
        st.write("Ayun lang.")

        st.write(''); st.write(''); st.write('')
        st.subheader('Example A:')
        st.latex(r"\int x \csc^2 x \, dx")
        st.write('If we try, for example, applying u-sub on the given problem, we will notice that it leads to nowhere. The given is a product of two expressions, and this is where IBP comes in.')
        st.write('The given consists of an **A**lgebraic expression $x$ and a **T**rig function $\\csc^2 x$. According to LIATE, A (Algebraic) comes first, so that is our $u$, at bale $dv$ yung natira.')
        col1, col2 = st.columns(2)
        with col1:
            st.latex(r"u=x")
            st.latex(r"\,du=\,dx")
        with col2:
            st.latex(r"\,dv=\csc^2 x\,dx")
            st.latex(r"v=-\cot x")
        st.write('')
        st.write('Thus,')
        st.latex(r"=-x \cot x - \int -\cot x \, dx")
        st.latex(r'=\boxed{-x \cot x+\ln{|\sin x}|+C}')

        st.write(''); st.write(''); st.write('')
        st.subheader('Example B:')
        st.latex(r"\int_1^e \ln^2 x \, dx")
        st.write('The given only has the **L**ogarithmic function $\\ln^2 x$ and that can be our $u$. What remained is the $dx$ and that will be our $dv$.')
        col1, col2 = st.columns(2)
        with col1:
            st.latex(r"u=\ln^2 x")
            st.latex(r"\,du=\frac{2\ln x}{x}\,dx")
        with col2:
            st.latex(r"\,dv=\,dx")
            st.latex(r"v=x")
        st.write('')
        st.write('Thus,')
        st.latex(r"=x \ln^2 x\Big|_1^e - \int_1^e \left(\frac{2\ln x}{x}\right) x \, dx")
        st.latex(r"=x \ln^2 x\Big|_1^e - 2\int_1^e \ln x \, dx")
        st.write('For the integral of $\\ln x$, it is still not solvable with u-sub. Hence, we again apply IBP.')
        col1, col2 = st.columns(2)
        with col1:
            st.latex(r"\bar{u}=\ln x")
            st.latex(r"\,d \bar{u}=\frac{1}{x}\,dx")
        with col2:
            st.latex(r"\,d\bar{v}=\,dx")
            st.latex(r"\bar{v}=x")
        st.write('')
        st.write("We have:")
        st.latex(r"=x \ln^2 x\Big|_1^e - 2\left(x \ln x\Big|_1^e - \int_1^e \, dx\right)")
        st.latex(r"=x \ln^2 x\Big|_1^e - 2\left(x \ln x\Big|_1^e - x\Big|_1^e \right)")
        st.write('Be very careful with the parentheses and signs.')
        st.latex(r"=\Big[x \ln^2 x- 2x \ln x + 2x \Big|_1^e")
        st.latex(r'=\Big[e \ln^2(e)- 2e \ln(e) + 2e\Big]-\Big[ \ln^2(1)- 2 \ln(1) + 2\Big]')
        st.latex(r'=\Big[e-2e+2e\Big]-\Big[0-0+2\Big]')
        st.latex(r'=\boxed{e-2}')

        st.write(''); st.write(''); st.write('')
        st.subheader('Example C:')
        st.latex(r"\int e^{3x}\sin(9x) \, dx")
        st.write('According to LIATE:')
        col1, col2 = st.columns(2)
        with col1:
            st.latex(r"u=\sin(9x)")
            st.latex(r"\,du=9\cos(9x)\,dx")
        with col2:
            st.latex(r"\,dv=e^{3x}\,dx")
            st.latex(r"v=\frac{1}{3}e^{3x}")
        st.write('')
        st.write('Thus,')
        st.latex(r'=\frac{1}{3}e^{3x}\sin(9x)-3\int e^{3x}\cos(9x) \,dx')
        st.write('Next, the new integral requires another IBP.')
        col1, col2 = st.columns(2)
        with col1:
            st.latex(r"\bar{u}=\cos(9x)")
            st.latex(r"\,d\bar{u}=-9\sin(9x)\,dx")
        with col2:
            st.latex(r"\,d\bar{v}=e^{3x}\,dx")
            st.latex(r"\bar{v}=\frac{1}{3}e^{3x}")
        st.write('')
        st.write('Now, we have:')
        st.latex(r'=\frac{1}{3}e^{3x}\sin(9x)-3\left(\frac{1}{3}e^{3x}\cos(9x)+3\int e^{3x}\sin(9x) \,dx\right)')
        st.write('Simplifying a bit:')
        st.latex(r'=\frac{1}{3}e^{3x}\sin(9x)-e^{3x}\cos(9x)-9\int e^{3x}\sin(9x) \,dx')
        st.write('Note that all of these is equal to the original problem.')
        st.latex(r'\int e^{3x}\sin(9x) \, dx=\frac{1}{3}e^{3x}\sin(9x)-e^{3x}\cos(9x)-9\int e^{3x}\sin(9x) \,dx')
        st.write('Algebra as follows:')
        st.latex(r'10\int e^{3x}\sin(9x) \, dx=\frac{1}{3}e^{3x}\sin(9x)-e^{3x}\cos(9x)')
        st.write('Therefore,')
        st.latex(r'\int e^{3x}\sin(9x) \, dx=\boxed{\frac{1}{30}e^{3x}\sin(9x)-\frac{1}{10}e^{3x}\cos(9x)+C}')

        st.write(''); st.write(''); st.write('')
        st.subheader('Example D: (Using the Tabular Method)')
        st.latex(r"\int x^3 e^{x} \, dx")
        st.write('Tabular method is a shortcut for applying IBP multiple times. It works best when IBP needs to be performed repeatedly to solve the integral.')
        st.write('The method follows the same rules for choosing $u$ and $dv$, but instead of applying IBP step by step, you repeatedly differentiate $u$ and integrate $dv$ as part of the shortcut. Assign alternating signs to each row, then multiply diagonally, similar to $uv$ in IBP, and combine them all. The last row is multiplied and forms the last integral.')
        col1, col2, col3 = st.columns([5,1,5])
        with col1:
            st.latex(r'+')
            st.latex(r'-')
            st.latex(r'+')
            st.latex(r'-')
            st.latex(r'+')
        with col2:
            st.latex(r'u=x^3')
            st.latex(r'3x^2')
            st.latex(r'6x')
            st.latex(r'6')
            st.latex(r'0')
        with col3:
            st.latex(r"\,dv=e^x\,dx")
            st.latex(r"e^x")
            st.latex(r"e^x")
            st.latex(r"e^x")
            st.latex(r"e^x")
        st.write('')
        st.write('Now, multiplying diagonally and taking into account of the alternating signs:')
        st.latex(r'=x^3e^x-3x^2e^x+6xe^x-6e^x+\int (0)(e^x)\,dx')
        st.write('We already have our final answer.')
        st.latex(r'=\boxed{x^3e^x-3x^2e^x+6xe^x-6e^x+C}')
        st.write('')
        st.write('The tabular method can also be applied to the previous examples, and the row at which you stop differentiating/integrating depends on the integral. If the given does not require many IBPs, then this method is essentially the same as the standard $u$-$dv$ approach.')
        st.write('')
        st.markdown('If you are interested, check out this [1 min yt short by bprp](https://youtu.be/N1KLaLi_LjA?si=AF78SVhlNmoBGgbq) on how to utilize the tabular method more effectively.')

    elif st.session_state.page == "trig":
        st.subheader("Trig Integ")
        st.write("Trigonometric integrals involve integrating trig functions and applying special techniques, depending on their exponents.")
        st.write('Recall the following trigonometric identities:')
        st.markdown("""
        - $\\sin^2x+\\cos^2x=1$
        - $\\tan^2x+1=\\sec^2x$
        - $1+\\cot^2x=\\csc^2x$
        """)
        st.markdown("""
        - $\\sin^2x=\\frac{{1}}{{2}}(1-\\cos(2x))\\quad$(NEW)
        - $\\cos^2x=\\frac{{1}}{{2}}(1+\\cos(2x))\\quad$(NEW)        
        """)
        st.write('The module provides instructions on the procedures to follow depending the trig present and their exponents. However, it is not really required to memorize them to answer different cases of trig integ.')
        st.write('Trig integ is all about determining when to apply u-sub and when to use trigonometric identities. When performing u-sub, you can anticipate what $du$ will be and whether it will simplify the integral. Ofc, this requires practice if we are opting not to memorize anything. However, there are some special cases that we simply need to remember.')
        
        st.write(''); st.write(''); st.write('')
        st.subheader('Example A:')
        st.latex(r"\int \sec^3x\tan^3x \, dx")
        st.write("Let's try u-sub, $u=\\tan x$. Looking ahead, $du$ will be $\\sec^2 x$, which means it will cancel two secants on the integrand, leaving one left, $\\sec x$. All the $\\tan x$ can be subsituted into $u$, but it is not possible to turn a single $\\sec x$ in terms of $u$. Usually, when the other trig has an odd number of exponent left, the choice of u-sub is incorrect.")
        st.write("Next, let's try $u=\\sec x$. Looking ahead, $du$ will be $\\sec x\\tan x$, which will cancel one each with the integrand, leaving two of each left, $\\sec^2 x\\tan^2 x$. All the $\\sec x$ can be substituted into $u$, and the remaining $\\tan^2 x$ can be turned into $\\sec^2 x-1$ using trigonometric identity. Since the exponent of $\\tan x$ is even, it became possible to express all expressions in terms of $u$.")
        st.write('All of these is an example of a thought process when looking ahead.')
        st.latex(r"u = \sec x, \quad \, du = \sec x\tan x \, dx")
        st.write('Thus,')
        st.latex(r'=\int \sec^2 x\tan^2 x \, du')
        st.latex(r'=\int \sec^2 x(\sec^2 x-1)) \, du')
        st.latex(r'=\int u^2(u^2-1)) \, du')
        st.latex(r'=\int (u^4-u^2) \, du')
        st.latex(r'=\frac{1}{5}u^5-\frac{1}{3}u^3+C')
        st.write('Substituting back:')
        st.latex(r'=\boxed{\frac{1}{5}\sec^5 x-\frac{1}{3}\sec^3 x+C}')

        st.write(''); st.write(''); st.write('')
        st.subheader('Example B:')
        st.latex(r"\int \sin^4 x \, dx")
        st.write("If the exponents of $\\sin x$ and $\\cos x$ are both even, then we apply the (NEW) trigonometric identities we've learned. If for example that one of them has an odd exponent, then it's just u-sub.")
        st.write("Exponent of $\\cos x$ in our given is 0 since it's not there, so technically even.")
        st.latex(r"= \int (\sin^2 x)^2 \, dx")
        st.latex(r"= \int \left(\frac{1}{2}(1-\cos(2x))\right)^2 \, dx")
        st.latex(r"= \frac{1}{4} \int (1-2\cos(2x)+\cos^2(2x)) \, dx")
        st.write('We can easily integrate the first two terms.')
        st.latex(r"= \frac{1}{4}(x-\sin(2x)) + \frac{1}{4} \int \cos^2(2x) \, dx")
        st.write('Since the exponent of $\\cos x$ is still even, we apply again the (NEW) trig identity.')
        st.latex(r"= \frac{1}{4}(x-\sin(2x)) + \frac{1}{4} \int \frac{1}{2}(1+\cos(4x)) \, dx")
        st.latex(r"= \frac{1}{4}(x-\sin(2x)) + \frac{1}{8} \left(x+\frac{1}{4}\sin(4x)\right)+C")
        st.write('Simplifying a bit:')
        st.latex(r"= \boxed{\frac{3}{8}x-\frac{1}{4}\sin(2x) + \frac{1}{32}\sin(4x)+C}")

        st.write(''); st.write(''); st.write('')
        st.subheader('Example C:')
        st.latex(r"\int \csc^3 x \, dx")
        st.write('If the exponent of $\\sec x$ OR $\\csc x$ is odd AND the exponent of $\\tan x$ OR $\\cot x$ is even, then the only way to solve the trig integ is thru IBP.')
        st.write('Otherwise, if the exponent of $\\sec x$ OR $\\csc x$ is even OR the exponent of $\\tan x$ OR $\\cot x$ is odd, then they are much simpler. Either by trigonometric identity or just u-sub. (More of these cases on the Exercise)')
        st.write('When performing IBP on a trig integ, put an expression on $dv$ that is easy to integrate.')
        col1, col2, col3 = st.columns([3,1,8])
        with col1:
            st.latex(r'+')
            st.latex(r'-')
        with col2:
            st.latex(r'u=\csc x')
            st.latex(r'du=-\csc x\cot x')
        with col3:
            st.latex(r"dv=\csc^2 x \,dx")
            st.latex(r"v=-\cot x")
        st.write('')
        st.write('Thus,')
        st.latex(r'=-\csc x\cot x - \int \csc x\cot^2 x \, dx')
        st.write('The exponent of $\\csc x$ and $\\cot x$ are odd and even, but we have already applied IBP. To proceed, we will apply trigonometric identity on the even exponent trig.')
        st.latex(r'=-\csc x\cot x - \int \csc x(\csc^2 x-1) \, dx')
        st.latex(r'=-\csc x\cot x - \int (\csc^3 x-\csc x) \, dx')
        st.latex(r'=-\csc x\cot x +\ln{|\csc x-\cot x|} - \int \csc^3 x \, dx')
        st.write('Note that all of these is equal to the original problem.')
        st.latex(r'\int \csc^3 x \, dx=-\csc x\cot x +\ln{|\csc x-\cot x|} - \int \csc^3 x \, dx')
        st.write('Performing algebra and simplifying:')
        st.latex(r'2\int \csc^3 x \, dx=-\csc x\cot x +\ln{|\csc x-\cot x|}')
        st.latex(r'\int \csc^3 x \, dx=\boxed{-\frac{1}{2}\csc x\cot x +\frac{1}{2}\ln{|\csc x-\cot x|}}')

    st.write(""); st.write(""); st.write(""); st.write(""); st.write("")

# Function to display the quiz menu where users can choose a quiz type
def show_menu():
    st.header("Select one to review:")
    
    # CSS for hover effect
    st.markdown("""
        <style>
        .hover-button {
            background-color: white;
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 10px;
            margin: 5px 0;
            cursor: pointer;
            position: relative;
            display: inline-block;
            width: auto;
            color: #A9A9A9;  /* Added gray color */
        }
        
        .hover-button:hover::after {
            content: "🚧 Coming Soon!";
            position: absolute;
            right: -130px;
            top: 50%;
            transform: translateY(-50%);
            background-color: #262730;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 14px;
        }
        </style>
        """, unsafe_allow_html=True)

    if st.button("U-Substitution (Math 21)"):
        set_page("u_sub")

    if st.button("Integration by Parts"):
        set_page("ibp")

    st.markdown("""
        <div class="hover-button">
            Trigonometric Integrals
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="hover-button">
            Trigonometric Substitution
        </div>
        """, unsafe_allow_html=True)
    
    col11, col12, col13 = st.columns([2, 6, 2])
    # Button to go back to the menu
    with col11:
        st.markdown("""
            <div class="hover-button">
                Partial Fractions
            </div>
            """, unsafe_allow_html=True)
    with col13:
        st.markdown("""
            <div class="hover-button">
                CHALLENGE
            </div>
            """, unsafe_allow_html=True)



# Function to change the current page
def set_page(page):
    st.session_state.page = page  # Set the current page (menu or quiz)
    st.session_state.feedback = ""  # Clear feedback when changing pages
    st.session_state.user_input = ""  # Clear user input
    st.session_state.answered_correctly = False  # Reset answer correctness state when navigating to menu
    st.rerun()  # Re-run the app to update the state

# Function to display the current quiz question and handle user input
def show_quiz():
    # Define the quiz data with integrals and their expected answers for different quiz types
    quiz_data = {
        "u_sub": [
            (r"\int \sin(2x) \,dx", "sin(2*x)"),
            (r"\int 2^{x^2}x \,dx", "x*2^(x^2)"),
            (r"\int \frac{x+1}{\sqrt{x-1}} \,dx", "(x+1)/sqrt(x-1)")
        ],
        "ibp": [
            (r"\int x^2\ln x \,dx", "x^2*ln(x)"),  # Question 1, integrand is x²
            (r"\int x \tan^{-1}x \,dx", "x*atan(x)"), # Question 2, integrand is 2x²
            (r"\int x^2 \sin(2x) \,dx", "x^2*sin(2*x)")  # Question 3, integrand is 3x²
        ],
        "trig": [
            (r"\int \cot^4x \,dx", "(cot(x))**4"), # Question 1, integrand is x³
            (r"\int \tan^3x \,dx", "(tan(x))**3"), # Question 2, integrand is 2x³
            (r"\int \sin^5x \cos^4x \,dx", "(sin(x))**5*(cos(x))**4")  # Question 3, integrand is 3x³
        ]
    }

    # Get the current question (integral expression) and expected answer
    integral_expr, f_x = quiz_data[st.session_state.page][st.session_state.question_index]

    st.subheader("EXERCISE:")
    st.write('Evaluate the following.')
    st.subheader(f'{st.session_state.question_index+1}.')
    st.latex(integral_expr)

    # Input box for the user to enter their answer
    user_answer = st.text_input(f"Enter your answer for Exercise No. {st.session_state.question_index + 1}:", key="answer_input")
    
    # Add the "Check Answer" button
    if st.button("Check Answer"):
        user_expr = ''
        if user_answer:
            try:
                # Preprocess the input to ensure multiplication is implied where needed
                user_answer = preprocess_input(user_answer.replace(" ",""))

                # Convert input string to sympy expression
                user_expr = sp.sympify(user_answer)

                # Store user input for display
                st.session_state.user_input = user_expr
                
                user_expr2 = sp.sympify(re.sub(r'Abs', r'', str(user_expr)))

                # Differentiate the student's answer (g x) to compare with the integrand
                g_x = sp.diff(user_expr2, x)

                # Convert f x (the expected answer) string into a sympy expression
                f_x_expr = sp.sympify(f_x)

                # Check if f x = g x at test points (1, 2, 3, 4, 5)
                correct_vals = [str(f_x_expr.subs(x, v).evalf(5)) for v in TEST_POINTS]
                user_vals = [str(g_x.subs(x, v).evalf(5)) for v in TEST_POINTS]
                # Check if results match
                if correct_vals == user_vals:
                    if st.session_state.question_index == 2:
                        st.session_state.feedback = "✅ ⭐ Gudjob! ⭐"
                    else:
                        st.session_state.feedback = "✅ Correct!"  # Provide positive feedback if correct
                    st.session_state.answered_correctly = True
                else:
                    #st.session_state.feedback = f"❌ {correct_vals} & {user_vals}"
                    st.session_state.feedback = "❌ Incorrect. Try again!"  # Provide negative feedback if incorrect
                    st.session_state.answered_correctly = False


            except Exception:
                # Handle any errors (e.g., invalid user input) and provide feedback
                #st.session_state.feedback = f"⚠️ {user_expr}"
                st.session_state.feedback = f"⚠️ Invalid input. Please enter a valid mathematical expression."
                st.session_state.answered_correctly = False

            st.session_state.user_input = user_expr  # Store the input for display
            st.rerun()  # Ensure the page re-runs to update the state


    # Display user input beautifully
    if st.session_state.user_input:
        st.write("Your input:")
        # Modified regex to handle both inverse trig and log/ln cases
        latex_output = sp.latex(st.session_state.user_input)
        latex_output = re.sub(r'(operatorname{a)(sin|cos|tan|csc|sec|cot)(h?)', r'\2\3^{-1', latex_output)
        latex_output = re.sub(r'\\log', r'\\ln', latex_output)  # Replace log with ln
        st.latex(latex_output)


    # Display feedback (correct/incorrect)
    st.write(st.session_state.feedback)

    # Show "Next" button if the answer is correct
    if st.session_state.answered_correctly:
        if st.session_state.question_index < len(quiz_data[st.session_state.page]) - 1:
            # If there is a next question, show the "Next" button
            if st.button("Next Item"):
                st.session_state.question_index += 1  # Go to the next question
                st.session_state.answered_correctly = False  # Reset after going to the next question
                st.session_state.user_input = ''
                st.session_state.feedback = ""
                st.rerun()  # Ensure page updates correctly


    col21, col22, col23 = st.columns([1, 8, 1])
    # Button to go back to the menu
    with col23:
        if st.button("Back"):
            st.session_state.question_index = 0
            set_page("menu")



if __name__ == "__main__":
    main()
