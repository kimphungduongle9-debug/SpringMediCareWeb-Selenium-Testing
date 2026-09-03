from selenium.webdriver.common.by import By

from pages.BasePage import BasePage


class PatientMedicalRecordDetailPage(BasePage):

    PAGE_TITLE = (
        By.XPATH,
        "//h2[normalize-space()='Chi tiết hồ sơ bệnh án']"
    )

    RECORD_BADGE = (
        By.XPATH,
        "//span[contains(@class, 'badge') "
        "and contains(normalize-space(.), 'Hồ sơ #')]"
    )

    PATIENT_NAME = (
        By.XPATH,
        "//p[normalize-space()='Bệnh nhân']/preceding-sibling::h5"
    )

    DOCTOR_NAME = (
        By.XPATH,
        "//strong[normalize-space()='Bác sĩ phụ trách:']/parent::p"
    )

    DIAGNOSIS = (
        By.XPATH,
        "//strong[normalize-space()='Chẩn đoán:']/parent::p"
    )

    TREATMENT = (
        By.XPATH,
        "//strong[normalize-space()='Hướng điều trị:']/parent::p"
    )

    CREATED_DATE = (
        By.XPATH,
        "//strong[normalize-space()='Ngày tạo:']/parent::p"
    )

    def get_page_title(self):
        return self.find(*self.PAGE_TITLE).text.strip()

    def get_record_id(self):
        text = self.find(*self.RECORD_BADGE).text.strip()

        return text.replace("Hồ sơ #", "").strip()

    def get_patient_name(self):
        return self.find(*self.PATIENT_NAME).text.strip()

    def get_doctor_information(self):
        return self.find(*self.DOCTOR_NAME).text.strip()

    def get_diagnosis_information(self):
        return self.find(*self.DIAGNOSIS).text.strip()

    def get_treatment_information(self):
        return self.find(*self.TREATMENT).text.strip()

    def get_created_date_information(self):
        return self.find(*self.CREATED_DATE).text.strip()