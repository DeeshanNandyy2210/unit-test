import streamlit as st
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

# Streamlit config
st.set_page_config(page_title="🧠 Symbolic Math Engine", layout="wide")

st.title("🧠 Symbolic Math Calculator")

# --- Sidebar Options ---
st.sidebar.header("Options")

mode = st.sidebar.selectbox("Choose Mode", ["Differentiate", "Integrate", "Implicit Differentiate", "Gradient/Jacobian"])
expr_input = st.text_input("Enter expression (e.g., sin(x)*x^2):", value="x^2 + sin(x)")
variables_input = st.text_input("List all variables (comma-separated):", value="x,y")
diff_var = st.text_input("Differentiate / Integrate w.r.t:", value="x")

# Auto-correction
def autocorrect_input(expr: str) -> str:
    return expr.replace("^", "**")

expr_input = autocorrect_input(expr_input)

try:
    var_list = [sp.Symbol(v.strip()) for v in variables_input.split(",")]
    var_dict = {str(v): v for v in var_list}
    var = var_dict.get(diff_var.strip(), sp.Symbol(diff_var.strip()))
    expr = sp.sympify(expr_input, locals=var_dict)

    if mode == "Differentiate":
        st.subheader("✅ Derivative")
        derivative = sp.diff(expr, var)
        st.latex(f"\\frac{{d}}{{d{diff_var}}}({sp.latex(expr)}) = {sp.latex(derivative)}")

        if len(var_list) == 1:
            x = var_list[0]
            f_lamb = sp.lambdify(x, expr, modules=["numpy"])
            d_lamb = sp.lambdify(x, derivative, modules=["numpy"])
            x_vals = np.linspace(-10, 10, 400)
            try:
                y_vals = f_lamb(x_vals)
                dy_vals = d_lamb(x_vals)
                fig, ax = plt.subplots()
                ax.plot(x_vals, y_vals, label="f(x)")
                ax.plot(x_vals, dy_vals, '--', label="f'(x)")
                ax.legend()
                st.pyplot(fig)
            except:
                st.warning("Could not plot due to domain issues.")

    elif mode == "Integrate":
        st.subheader("✅ Indefinite Integral")
        integral = sp.integrate(expr, var)
        st.latex(f"\\int {sp.latex(expr)} \\, d{diff_var} = {sp.latex(integral)} + C")

    elif mode == "Implicit Differentiate":
        st.subheader("✅ Implicit Differentiation")
        # Assume equation format: lhs = rhs
        if "=" not in expr_input:
            st.warning("Use implicit format: e.g., x^2 + y^2 = 25")
        else:
            lhs_str, rhs_str = expr_input.split("=")
            lhs = sp.sympify(autocorrect_input(lhs_str), locals=var_dict)
            rhs = sp.sympify(autocorrect_input(rhs_str), locals=var_dict)
            equation = sp.Eq(lhs, rhs)
            y = [v for v in var_list if v != var][0]  # choose other variable
            dydx = sp.diff(lhs - rhs, var).simplify()
            dy_symbol = sp.Symbol(f"{sp.latex(sp.diff(y, var))}")
            st.latex(f"\\text{{Implicit equation: }} {sp.latex(equation)}")
            st.latex(f"\\text{{Implicit derivative }} \\frac{{d{y}}}{{d{var}}} = {sp.latex(sp.solve(sp.diff(lhs - rhs), sp.diff(y, var))[0])}")

    elif mode == "Gradient/Jacobian":
        st.subheader("✅ Gradient / Jacobian")
        try:
            expr_vector = expr if isinstance(expr, (list, tuple)) else sp.Matrix([expr])
            jac = expr_vector.jacobian(var_list)
            st.latex(f"f = {sp.latex(expr_vector)}")
            st.latex(f"\\text{{Jacobian: }} {sp.latex(jac)}")
        except Exception as e:
            st.error(f"Could not compute Jacobian: {e}")

    # --- PDF Export ---
    st.subheader("📄 Export to PDF")
    if st.button("Export Result as PDF"):
        file_name = "math_output.pdf"
        doc = SimpleDocTemplate(file_name, pagesize=letter)
        styles = getSampleStyleSheet()
        flowables = [
            Paragraph("Symbolic Math Output", styles['Title']),
            Spacer(1, 12),
            Paragraph(f"Expression: ${sp.latex(expr)}$", styles['Normal']),
            Paragraph(f"Variable(s): {variables_input}", styles['Normal']),
            Paragraph(f"Mode: {mode}", styles['Normal']),
            Spacer(1, 12),
        ]
        if mode == "Differentiate":
            flowables.append(Paragraph(f"Derivative: ${sp.latex(derivative)}$", styles['Heading2']))
        elif mode == "Integrate":
            flowables.append(Paragraph(f"Integral: ${sp.latex(integral)} + C$", styles['Heading2']))
        elif mode == "Gradient/Jacobian":
            flowables.append(Paragraph(f"Jacobian Matrix: ${sp.latex(jac)}$", styles['Heading2']))
        elif mode == "Implicit Differentiate":
            dy_expr = sp.solve(sp.diff(lhs - rhs), sp.diff(y, var))[0]
            flowables.append(Paragraph(f"Implicit Derivative: ${sp.latex(dy_expr)}$", styles['Heading2']))
        doc.build(flowables)
        with open(file_name, "rb") as pdf_file:
            st.download_button("Download PDF", pdf_file, file_name, mime="application/pdf")

except Exception as e:
    st.error(f"❌ Error: {e}")
