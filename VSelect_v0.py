
import marimo                                     
app = marimo.App(width="medium")

@app.cell
def _():
    import marimo as mo                           
    mo.md(
        "# Variable selection scenario\n"
        
    )


# ------------------------------------------------------------
# Task 1
# ------------------------------------------------------------

@app.cell
def task_1():
    mo.vstack(
        [
            # 1) subtitle
            mo.md("## The story so far"),

            # 2) “Note to the team”
            mo.md(
                "The university is a large research institution that competes for students in a crowded " \
                "higher-education market. Over the past five years the first-to-second-year retention rate has " \
                "drifted downward, and graduation timelines have lengthened. Senior leadership has asked the Office of " \
                "the Provost to treat student persistence as a strategic priority rather than a routine metric. " \
                "An internal mandate now calls for data-informed, proactive outreach so that support staff can offer " \
                "help long before a student considers leaving. Within the Office of the Provost a small Student Success Analytics " \
                "group has been established. This team combines institutional researchers, academic advisors, compliance officers, "
                "and data engineers. Its first assignment is to create an early warning intelligence tool that flags continuing " \
                "undergraduates who appear at risk of stopping out or falling behind schedule. Advisors will then contact those " \
                "students and connect them with tutoring, financial counseling, or mentoring. The analytics group is expected to " \
                "respect privacy regulations such as FERPA and recent federal guidance that limits the use of individual financial-aid " \
                "records in automated decision systems. It is also expected to uphold the university commitment to equity and transparency in " \
                "every technical choice."
            ),

          
            mo.md("&nbsp;"),

            mo.md("## Role"),

            # 2) “Note to the team”
            mo.md(
                "You serve as the team’s data science specialist. Your immediate task is not to build a model but to decide which " \
                "pieces of information should be fed into one. Working with colleagues you have assembled a data dictionary drawn " \
                "from the university warehouse. The dictionary lists common attributes such as high school grade point averages, " \
                "standardized test scores, race, gender, residency status, and course loads. It also contains financial indicators " \
                "like Pell eligibility and Expected Family Contribution. Several context-specific items are included as well."\
                "Examples are whether a student applied to a regional campus after a main-campus denial, whether a student is a varsity athlete,"\
                "and the distance between the student’s home address and campus. No raw records are available at this stage of the project;"\
                "only the variable descriptions, their known limitations, and any red-flag notes provided by legal or ethical reviewers."
            ),

          
            mo.md("&nbsp;"),


            mo.md("## Business Objective & Product"),

            # 2) “Note to the team”
            mo.md(
                "Academic advisors need a concise, defensible list of candidate predictors that can drive a predictive model without violating " \
                "regulations or undermining equitable treatment. Your deliverable for this scenario is a Variable Selection Brief. " \
                "In one page you will designate each variable as included, excluded, or flagged for additional discussion. " \
                "For every decision you will provide a short rationale that links back to the goals of privacy protection, fairness, and practical usefulness. " \
                "Advisors and compliance staff will review and sign this brief before any modelling work proceeds."
            ),

          
            mo.md("&nbsp;"),

            # 3) instructions for the table
            mo.md("*For each variable choose **one** action:*"),

            # 4) centralized table
            mo.Html(
                """
                <div style="display:flex; justify-content:center;">
                  <table style="border-collapse:separate; border-spacing:0 6px; text-align:center;">
                    <thead>
                      <tr>
                        <th style="padding:0.5rem 1.5rem;">Action</th>
                        <th style="padding:0.5rem 1.5rem;">Meaning</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td style="padding:0.5rem 1.5rem;"><b>Include</b></td>
                        <td style="padding:0.5rem 1.5rem;">
                          Use this variable in the predictive model.
                        </td>
                      </tr>
                      <tr>
                        <td style="padding:0.5rem 1.5rem;"><b>Exclude</b></td>
                        <td style="padding:0.5rem 1.5rem;">
                          Remove it from consideration.
                        </td>
                      </tr>
                      <tr>
                        <td style="padding:0.5rem 1.5rem;"><b>Flag for Legal / IRB Review</b></td>
                        <td style="padding:0.5rem 1.5rem;">
                          Put the variable on hold until university counsel (or the IRB) provides guidance.
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                """
            ),
        ]
    )

@app.cell
def pell_status():

    # 1 reactive state for this variable
    get_choice, set_choice = mo.state(None)

    # 2 flag buttons
    include_btn = mo.ui.button(
        label="Include", kind="success", on_click=lambda _: set_choice("include")
    )
    exclude_btn = mo.ui.button(
        label="Exclude", kind="danger",  on_click=lambda _: set_choice("exclude")
    )
    flag_btn = mo.ui.button(
        label="Flag for Review", kind="warn", on_click=lambda _: set_choice("flag")
    )

    # 3 put buttons in an accordion 
    content = mo.vstack([
        mo.md(
            "Whether a student receives a federal Pell Grant. "
            "New regulations restrict use of financial-aid data in predictive modeling."
        ),
        mo.hstack([include_btn, exclude_btn, flag_btn], gap="1rem"),
    ])
    mo.accordion({"Pell Status": content})

    # 4 return the getter so other cells can react to it
    return get_choice

@app.cell
def pell_feedback(get_choice):

    # 1 read the current flag
    choice = get_choice()

    # 2 maps for emoji and label
    emoji_map = {
        "include": "🟢",
        "exclude": "🔴",
        "flag":    "🟡",
        None:      "⚪️",
    }
    text_map = {
        "include": "Include",
        "exclude": "Exclude",
        "flag":    "Flag for Review",
        None:      "no selection",
    }

    # 3 wrap in mo.md so this cell re-runs whenever choice changes
    mo.md(f"You decided to {emoji_map[choice]} **{text_map[choice]}** the variable.")


@app.cell
def pell_justification(get_choice):
    # 1 read current Pell selection
    pell_text_choice = get_choice()

    # 2 state holder for the justification text
    get_text_just_pell, set_text_just_pell = mo.state("")

    # 3 show textarea only after user picks Include / Exclude / Flag
    content_just_pell = (
        mo.ui.text_area(
            label="Please briefly justify your reasoning for your Pell Status choice",
            value=get_text_just_pell(),
            on_change=lambda v: set_text_just_pell(v),
            rows=4,
        )
        if pell_text_choice is not None
        else mo.md("")          
    )

    content_just_pell   

@app.cell
def efc_status():

    # 1 reactive state for this variable
    get_efc_choice, set_efc_choice = mo.state(None)

    # 2 flag buttons
    efc_include_btn = mo.ui.button(
        label="Include", kind="success", on_click=lambda _: set_efc_choice("include")
    )
    efc_exclude_btn = mo.ui.button(
        label="Exclude", kind="danger",  on_click=lambda _: set_efc_choice("exclude")
    )
    efc_flag_btn = mo.ui.button(
        label="Flag for Review", kind="warn", on_click=lambda _: set_efc_choice("flag")
    )

    # 3 put buttons in an accordion (or any layout you like)
    efc_content = mo.vstack([
        mo.md(
            "Amount a family is expected to contribute to education costs "
            "(legacy FAFSA metric). Regulatory compliance requires excluding "
            "this sensitive financial information."
        ),
        mo.hstack([efc_include_btn, efc_exclude_btn, efc_flag_btn], gap="1rem"),
    ])
    mo.accordion({"Expected Family Contribution (EFC)": efc_content})

    # 4 return the getter so other cells can react to it
    return get_efc_choice

@app.cell
def efc_feedback(get_efc_choice):

    # 1 read the current flag
    efc_choice = get_efc_choice()

    # 2 maps for emoji and label
    efc_emoji_map = {
        "include": "🟢",
        "exclude": "🔴",
        "flag":    "🟡",
        None:      "⚪️",
    }
    efc_text_map = {
        "include": "Include",
        "exclude": "Exclude",
        "flag":    "Flag for Review",
        None:      "no selection",
    }

    # 3 wrap in mo.md so this cell re-runs whenever choice changes
    mo.md(f"You decided to {efc_emoji_map[efc_choice]} **{efc_text_map[efc_choice]}** the variable.")


@app.cell
def efc_justification(get_efc_choice):
    # 1 read current EFC selection
    efc_text_choice = get_efc_choice()

    # 2 state holder for the justification text
    get_text_just_efc, set_text_just_efc = mo.state("")

    # 3 show textarea only after user picks Include / Exclude / Flag
    content_just_efc = (
        mo.ui.text_area(
            label="Please briefly justify your reasoning for your EFC choice",
            value=get_text_just_efc(),
            on_change=lambda v: set_text_just_efc(v),
            rows=4,
        )
        if efc_text_choice is not None
        else mo.md("")          
    )

    content_just_efc   

@app.cell
def sai_status():
    # 1) reactive state for SAI
    get_sai_choice, set_sai_choice = mo.state(None)

    # 2) flag buttons (all kwargs)
    sai_inc_btn  = mo.ui.button(
        label="Include",
        kind="success",
        on_click=lambda _: set_sai_choice("include"),
    )
    sai_exc_btn  = mo.ui.button(
        label="Exclude",
        kind="danger",
        on_click=lambda _: set_sai_choice("exclude"),
    )
    sai_flag_btn = mo.ui.button(
        label="Flag for Review",
        kind="warn",
        on_click=lambda _: set_sai_choice("flag"),
    )

    # 3) accordion content
    sai_content = mo.vstack([
        mo.md(
            "A new metric from recent FAFSA changes that replaced EFC. "
            "Recent implementation means this data may not be available for all "
            "students in your historical dataset."
        ),
        mo.hstack([sai_inc_btn, sai_exc_btn, sai_flag_btn], gap="1rem"),
    ])
    mo.accordion({"Student Aid Index (SAI)": sai_content})

    # 4) expose getter
    return get_sai_choice

@app.cell
def sai_feedback(get_sai_choice):
    # current flag
    sai_choice = get_sai_choice()

    # emoji / text maps
    sai_emoji_map = {
        "include": "🟢",
        "exclude": "🔴",
        "flag":    "🟡",
        None:      "⚪️",
    }
    sai_text_map = {
        "include": "Include",
        "exclude": "Exclude",
        "flag":    "Flag for Review",
        None:      "no selection",
    }

    # show live feedback line
    mo.md(
        f"You decided to {sai_emoji_map[sai_choice]} "
        f"**{sai_text_map[sai_choice]}** the variable."
    )

@app.cell
def sai_justification(get_sai_choice):
    # read current SAI selection (unique local name)
    sai_selected_flag = get_sai_choice()

    # state holder for SAI justification text
    get_text_just_sai, set_text_just_sai = mo.state("")

    # show textarea only after a flag is chosen
    content_just_sai = (
        mo.ui.text_area(
            label="Please briefly justify your reasoning for your SAI choice",
            value=get_text_just_sai(),
            on_change=lambda v: set_text_just_sai(v),
            rows=4,
        )
        if sai_selected_flag is not None
        else mo.md("")          # nothing yet
    )

    content_just_sai   # final expression rendered by the cell


# Unmet Need 
@app.cell
def unmet_status():
    # reactive state for Unmet Need
    get_unmet_choice, set_unmet_choice = mo.state(None)

    # buttons (all kwargs)
    unmet_inc_btn  = mo.ui.button(
        label="Include",
        kind="success",
        on_click=lambda _: set_unmet_choice("include"),
    )
    unmet_exc_btn  = mo.ui.button(
        label="Exclude",
        kind="danger",
        on_click=lambda _: set_unmet_choice("exclude"),
    )
    unmet_flag_btn = mo.ui.button(
        label="Flag for Review",
        kind="warn",
        on_click=lambda _: set_unmet_choice("flag"),
    )

    # accordion content
    unmet_content = mo.vstack([
        mo.md(
            "Gap between the cost of attendance and the student’s available resources. "
            "Financial-stress indicator, but regulatory restrictions likely prohibit "
            "its use in individual-level models."
        ),
        mo.hstack([unmet_inc_btn, unmet_exc_btn, unmet_flag_btn], gap="1rem"),
    ])
    mo.accordion({"Unmet Need": unmet_content})

    # expose getter
    return get_unmet_choice

@app.cell
def unmet_feedback(get_unmet_choice):
    unmet_choice = get_unmet_choice()

    unmet_emoji_map = {
        "include": "🟢",
        "exclude": "🔴",
        "flag":    "🟡",
        None:      "⚪️",
    }
    unmet_text_map = {
        "include": "Include",
        "exclude": "Exclude",
        "flag":    "Flag for Review",
        None:      "no selection",
    }

    mo.md(
        f"You decided to {unmet_emoji_map[unmet_choice]} "
        f"**{unmet_text_map[unmet_choice]}** the variable."
    )

@app.cell
def unmet_justification(get_unmet_choice):
    unmet_selected_flag = get_unmet_choice()

    # text state
    get_text_just_unmet, set_text_just_unmet = mo.state("")

    content_just_unmet = (
        mo.ui.text_area(
            label="Please briefly justify your reasoning for your Unmet Need choice",
            value=get_text_just_unmet(),
            on_change=lambda v: set_text_just_unmet(v),
            rows=4,
        )
        if unmet_selected_flag is not None
        else mo.md("")
    )

    content_just_unmet   # rendered

@app.cell
def merit_status():
    # state for Merit Award Amount
    get_merit_choice, set_merit_choice = mo.state(None)

    # buttons
    merit_inc_btn  = mo.ui.button(
        label="Include",
        kind="success",
        on_click=lambda _: set_merit_choice("include"),
    )
    merit_exc_btn  = mo.ui.button(
        label="Exclude",
        kind="danger",
        on_click=lambda _: set_merit_choice("exclude"),
    )
    merit_flag_btn = mo.ui.button(
        label="Flag for Review",
        kind="warn",
        on_click=lambda _: set_merit_choice("flag"),
    )

    # accordion content
    merit_content = mo.vstack([
        mo.md(
            "Scholarship amounts awarded based on academic achievement rather than "
            "financial need. Consider whether this variable primarily reflects prior "
            "achievement or introduces socioeconomic factors into your model."
        ),
        mo.hstack([merit_inc_btn, merit_exc_btn, merit_flag_btn], gap="1rem"),
    ])
    mo.accordion({"Merit Award Amount": merit_content})

    return get_merit_choice

@app.cell
def merit_feedback(get_merit_choice):
    merit_choice = get_merit_choice()

    merit_emoji_map = {
        "include": "🟢",
        "exclude": "🔴",
        "flag":    "🟡",
        None:      "⚪️",
    }
    merit_text_map = {
        "include": "Include",
        "exclude": "Exclude",
        "flag":    "Flag for Review",
        None:      "no selection",
    }

    mo.md(
        f"You decided to {merit_emoji_map[merit_choice]} "
        f"**{merit_text_map[merit_choice]}** the variable."
    )

@app.cell
def merit_justification(get_merit_choice):
    merit_selected_flag = get_merit_choice()

    get_text_just_merit, set_text_just_merit = mo.state("")

    content_just_merit = (
        mo.ui.text_area(
            label="Please briefly justify your reasoning for your Merit Award choice",
            value=get_text_just_merit(),
            on_change=lambda v: set_text_just_merit(v),
            rows=4,
        )
        if merit_selected_flag is not None
        else mo.md("")
    )

    content_just_merit  # rendered



@app.cell
def pplus_status():
    # state for Pell Plus
    get_pplus_choice, set_pplus_choice = mo.state(None)

    # buttons
    pplus_inc_btn  = mo.ui.button(
        label="Include",
        kind="success",
        on_click=lambda _: set_pplus_choice("include"),
    )
    pplus_exc_btn  = mo.ui.button(
        label="Exclude",
        kind="danger",
        on_click=lambda _: set_pplus_choice("exclude"),
    )
    pplus_flag_btn = mo.ui.button(
        label="Flag for Review",
        kind="warn",
        on_click=lambda _: set_pplus_choice("flag"),
    )

    # accordion content
    pplus_content = mo.vstack([
        mo.md(
            "University matching funds that complement federal Pell Grants. "
            "Financial-aid variables like this are likely subject to the same "
            "regulatory restrictions as other financial data."
        ),
        mo.hstack([pplus_inc_btn, pplus_exc_btn, pplus_flag_btn], gap="1rem"),
    ])
    mo.accordion({"Pell Plus": pplus_content})

    return get_pplus_choice

@app.cell
def pplus_feedback(get_pplus_choice):
    pplus_choice = get_pplus_choice()

    pplus_emoji_map = {
        "include": "🟢",
        "exclude": "🔴",
        "flag":    "🟡",
        None:      "⚪️",
    }
    pplus_text_map = {
        "include": "Include",
        "exclude": "Exclude",
        "flag":    "Flag for Review",
        None:      "no selection",
    }

    mo.md(
        f"You decided to {pplus_emoji_map[pplus_choice]} "
        f"**{pplus_text_map[pplus_choice]}** the variable."
    )

@app.cell
def pplus_justification(get_pplus_choice):
    pplus_selected_flag = get_pplus_choice()

    get_text_just_pplus, set_text_just_pplus = mo.state("")

    content_just_pplus = (
        mo.ui.text_area(
            label="Please briefly justify your reasoning for your Pell Plus choice",
            value=get_text_just_pplus(),
            on_change=lambda v: set_text_just_pplus(v),
            rows=4,
        )
        if pplus_selected_flag is not None
        else mo.md("")
    )

    content_just_pplus


# Detailed Feedback on all variables
@app.cell
def detailed_feedback(
    get_choice,          # Pell
    get_efc_choice,      # EFC
    get_sai_choice,      # SAI
    get_unmet_choice,    # Unmet
    get_merit_choice,    # MErit
    get_pplus_choice,    # PPlus
):

    # read each variable’s choice
    choice_pell  = get_choice()
    choice_efc   = get_efc_choice()
    choice_sai   = get_sai_choice()
    choice_unmet = get_unmet_choice()
    choice_merit  = get_merit_choice()
    choice_pplus  = get_pplus_choice()

    # ----- Pell message
    if choice_pell == "exclude":
        msg_pell = "Right call"
    elif choice_pell == "flag":
        msg_pell = "Flagged"
    elif choice_pell == "include":
        msg_pell = (
            "Including Pell Status violates current federal guidance and may expose "
            "the institution to penalties. Consider aggregate reporting instead of "
            "individual-level use."
        )
    else:
        msg_pell = ""

    # ----- EFC message
    if choice_efc == "exclude":
        msg_efc = "Right call"
    elif choice_efc == "flag":
        msg_efc = "Flagged"
    elif choice_efc == "include":
        msg_efc = (
            "EFC is explicitly barred under 2024 Department of Education rules; "
            "its inclusion would render the model non-compliant."
        )
    else:
        msg_efc = ""

    # ----- SAI message
    if choice_sai == "exclude":
        msg_sai = "Right call"
    elif choice_sai == "flag":
        msg_sai = "Flagged"
    elif choice_sai == "include":
        msg_sai = (
            "SAI is sensitive financial-aid data with incomplete coverage. "
            "Using it risks privacy violations and injects missing-data bias."
        )
    else:
        msg_sai = ""

    # --- Unmet Need msg ---
    if choice_unmet == "exclude":
        msg_unmet = "Right call"
    elif choice_unmet == "flag":
        msg_unmet = "Flagged"
    elif choice_unmet == "include":
        msg_unmet = (
            "Unmet Need combines multiple restricted data points. Including it would "
            "contravene policy and amplify socioeconomic bias."
        )
    else:
        msg_unmet = ""
    
    # --- Merit Award msg ---
    if choice_merit == "exclude":
        msg_merit = "Right call"
    elif choice_merit == "flag":
        msg_merit = "Flagged"
    elif choice_merit == "include":
        msg_merit = (
            "Merit awards can proxy socioeconomic status and unintentionally "
            "disadvantage low-income students. Use only with a strong equity "
            "justification."
        )
    else:
        msg_merit = ""
        
    # --- Pell Plus msg ---
    if choice_pplus == "exclude":
        msg_pplus = "Right call"
    elif choice_pplus == "flag":
        msg_pplus = "Flagged"
    elif choice_pplus == "include":
        msg_pplus = (
            "Pell Plus directly signals Pell participation; individual-level use "
            "is restricted. Exclude or seek explicit legal clearance."
        )
    else:
        msg_pplus = ""


    # build accordion content
    content_detail_feedback = mo.vstack([
        mo.md(f"**Pell :** {msg_pell}"),
        mo.md(f"**EFC  :** {msg_efc}"),
        mo.md(f"**SAI  :** {msg_sai}"),
        mo.md(f"**Unmet :** {msg_unmet}"),
        mo.md(f"**Merit  :** {msg_merit}"),
        mo.md(f"**Pell+  :** {msg_pplus}"),
    ])

    mo.accordion({"Detailed Feedback": content_detail_feedback})


@app.cell
def task_f():
    mo.vstack(
        [
            # 1) subtitle
            mo.md("## Placeholder for Product"),

            # 2) “Note to the team”
            mo.md(
                "Paragraph"
            ),

          
            mo.md("&nbsp;"),

            # 1) subtitle
            mo.md("## Placeholder for Learner Reflection"),

            # 2) “Note to the team”
            mo.md(
                "Paragraph"
            ),

          
            mo.md("&nbsp;"),
        ]
    )


if __name__ == "__main__":
    app.run()         