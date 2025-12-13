import streamlit as st
from app_backend.datasets import (
    get_datasets,
    add_dataset,
    get_dataset_by_id,
    update_dataset,
    delete_dataset
)

st.set_page_config(page_title="Datasets Metadata", page_icon="📊", layout="wide")

# Require login
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must log in first.")
    st.stop()

st.title("Datasets Metadata Management")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["View Datasets", "Add Dataset", "Update Dataset", "Delete Dataset"])

# ===============================================================
# 1️⃣ VIEW DATASETS
# ===============================================================
with tab1:
    st.subheader("All Datasets")
    df = get_datasets()
    st.dataframe(df, use_container_width=True)

# ===============================================================
# 2️⃣ ADD DATASET
# ===============================================================
with tab2:
    st.subheader("Add New Dataset")

    name = st.text_input("Dataset Name")
    source = st.text_input("Source")
    record_count = st.number_input("Record Count", min_value=0, step=1)
    last_updated = st.text_input("Last Updated (YYYY-MM-DD)")
    description = st.text_area("Description")

    if st.button("Add Dataset"):
        ok = add_dataset(name, source, record_count, last_updated, description)
        if ok:
            st.success("Dataset added successfully!")
        else:
            st.error("Failed to add dataset.")

# ===============================================================
# 3️⃣ UPDATE DATASET
# ===============================================================
with tab3:
    st.subheader("Update Dataset")

    df = get_datasets()
    if df.empty:
        st.info("No datasets available to update.")
    else:
        dataset_ids = df["id"].tolist()
        selected_id = st.selectbox("Select Dataset ID to Edit", dataset_ids)

        # Fetch selected row
        dataset = get_dataset_by_id(selected_id)

        # Auto-fill current values
        new_name = st.text_input("Dataset Name", value=dataset["dataset_name"])
        new_source = st.text_input("Source", value=dataset["source"])
        new_record_count = st.number_input("Record Count", min_value=0, step=1, value=int(dataset["record_count"]))
        new_last_updated = st.text_input("Last Updated", value=dataset["last_updated"])
        new_description = st.text_area("Description", value=dataset["description"])

        if st.button("Update Dataset"):
            ok = update_dataset(
                selected_id,
                new_name,
                new_source,
                new_record_count,
                new_last_updated,
                new_description
            )
            if ok:
                st.success(f"Dataset ID {selected_id} updated successfully!")
            else:
                st.error("Failed to update dataset.")

# ===============================================================
# 4️⃣ DELETE DATASET
# ===============================================================
with tab4:
    st.subheader("Delete Dataset")

    df = get_datasets()
    if df.empty:
        st.info("No datasets available to delete.")
    else:
        del_id = st.number_input("Enter Dataset ID to Delete", min_value=1, step=1)

        if st.button("Delete Dataset"):
            if del_id not in df["id"].values:
                st.error(f"Dataset ID {del_id} does not exist.")
            else:
                ok = delete_dataset(del_id)
                if ok:
                    st.success(f"Dataset {del_id} deleted successfully!")
                else:
                    st.error("Failed to delete dataset.")
