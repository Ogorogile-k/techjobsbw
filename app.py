from flask import Flask, render_template, jsonify
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_db_connection():
    return psycopg2.connect(
        os.environ["DATABASE_URL"],
        cursor_factory=RealDictCursor
    )


# ============================================================
# ALL JOBS
# ============================================================

@app.route("/")
def home():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM jobs
        ORDER BY date_found DESC
    """)

    jobs = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "techjobs.html",
        jobs=jobs
    )


# ============================================================
# ALL JOBS JSON API
# ============================================================

@app.route("/jobs")
def get_jobs():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM jobs
        ORDER BY date_found DESC
    """)

    jobs = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(jobs)


# ============================================================
# BY COMPANY
# ============================================================

@app.route("/companies")
def companies():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            c.company_id,
            c.name,
            COUNT(j.id) AS job_count
        FROM companies c
        INNER JOIN jobs j
            ON c.company_id = j.company_id
        GROUP BY
            c.company_id,
            c.name
        ORDER BY
            c.name
    """)

    companies = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "companies.html",
        companies=companies
    )


# ============================================================
# INDIVIDUAL COMPANY
# ============================================================

@app.route("/company/<int:company_id>")
def company_jobs(company_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    # --------------------------------------------------------
    # Get company
    # --------------------------------------------------------

    cursor.execute("""
        SELECT
            company_id,
            name,
            industry,
            website,
            email,
            phone,
            headquarters,
            logo,
            description
        FROM companies
        WHERE company_id = %s
    """, (company_id,))

    company = cursor.fetchone()

    if company is None:

        cursor.close()
        conn.close()

        return "Company not found", 404


    # --------------------------------------------------------
    # Get company's jobs
    # --------------------------------------------------------

    cursor.execute("""
        SELECT *
        FROM jobs
        WHERE company_id = %s
        ORDER BY date_found DESC
    """, (company_id,))

    jobs = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "company.html",
        company=company,
        jobs=jobs
    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(debug=True)
