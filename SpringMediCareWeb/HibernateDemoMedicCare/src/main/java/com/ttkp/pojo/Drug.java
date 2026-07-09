package com.ttkp.pojo;

import jakarta.persistence.*;
import java.io.Serializable;
import java.math.BigDecimal;
import java.util.Date;
import java.util.Set;

@Entity
@Table(name = "drug")
@NamedQueries({
    @NamedQuery(name = "Drug.findAll", query = "SELECT d FROM Drug d"),
    @NamedQuery(name = "Drug.findByDrugId", query = "SELECT d FROM Drug d WHERE d.drugId = :drugId"),
    @NamedQuery(name = "Drug.findByName", query = "SELECT d FROM Drug d WHERE d.name = :name"),
    @NamedQuery(name = "Drug.findByPrice", query = "SELECT d FROM Drug d WHERE d.price = :price"),
    @NamedQuery(name = "Drug.findByImage", query = "SELECT d FROM Drug d WHERE d.image = :image")
})
public class Drug implements Serializable {

    private static final long serialVersionUID = 1L;

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "drug_id")
    private Integer drugId;

    @JoinColumn(name = "category_id", referencedColumnName = "category_id")
    @ManyToOne(optional = false)
    private Category categoryId;

    @Basic(optional = false)
    @Column(name = "name")
    private String name;

    @Lob
    @Column(name = "description")
    private String description;

    @Basic(optional = false)
    @Column(name = "price")
    private BigDecimal price;

    @Basic(optional = false)
    @Column(name = "quantity")
    private int quantity;

    @Basic(optional = false)
    @Column(name = "min_quantity")
    private int minQuantity;

    @Column(name = "production_date")
    @Temporal(TemporalType.DATE)
    private Date productionDate;

    @Column(name = "expiry_date")
    @Temporal(TemporalType.DATE)
    private Date expiryDate;

    @Column(name = "dosage_form")
    private String dosageForm;

    @Column(name = "unit")
    private String unit;

    @Column(name = "strength")
    private String strength;

    @Column(name = "manufacturer")
    private String manufacturer;

    @Basic(optional = false)
    @Column(name = "status")
    private String status;

    @Column(name = "image")
    private String image;

    @OneToMany(cascade = CascadeType.ALL, mappedBy = "drugId")
    private Set<PrescriptionDetail> prescriptionDetailSet;

    public Drug() {
    }

    public Drug(Integer drugId) {
        this.drugId = drugId;
    }

    public Drug(Integer drugId, String name, BigDecimal price) {
        this.drugId = drugId;
        this.name = name;
        this.price = price;
    }

    public Integer getDrugId() {
        return drugId;
    }

    public void setDrugId(Integer drugId) {
        this.drugId = drugId;
    }

    public Category getCategoryId() {
        return categoryId;
    }

    public void setCategoryId(Category categoryId) {
        this.categoryId = categoryId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public BigDecimal getPrice() {
        return price;
    }

    public void setPrice(BigDecimal price) {
        this.price = price;
    }

    public int getQuantity() {
        return quantity;
    }

    public void setQuantity(int quantity) {
        this.quantity = quantity;
    }

    public int getMinQuantity() {
        return minQuantity;
    }

    public void setMinQuantity(int minQuantity) {
        this.minQuantity = minQuantity;
    }

    public Date getProductionDate() {
        return productionDate;
    }

    public void setProductionDate(Date productionDate) {
        this.productionDate = productionDate;
    }

    public Date getExpiryDate() {
        return expiryDate;
    }

    public void setExpiryDate(Date expiryDate) {
        this.expiryDate = expiryDate;
    }

    public String getDosageForm() {
        return dosageForm;
    }

    public void setDosageForm(String dosageForm) {
        this.dosageForm = dosageForm;
    }

    public String getUnit() {
        return unit;
    }

    public void setUnit(String unit) {
        this.unit = unit;
    }

    public String getStrength() {
        return strength;
    }

    public void setStrength(String strength) {
        this.strength = strength;
    }

    public String getManufacturer() {
        return manufacturer;
    }

    public void setManufacturer(String manufacturer) {
        this.manufacturer = manufacturer;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getImage() {
        return image;
    }

    public void setImage(String image) {
        this.image = image;
    }

    public Set<PrescriptionDetail> getPrescriptionDetailSet() {
        return prescriptionDetailSet;
    }

    public void setPrescriptionDetailSet(Set<PrescriptionDetail> prescriptionDetailSet) {
        this.prescriptionDetailSet = prescriptionDetailSet;
    }

    @Override
    public int hashCode() {
        int hash = 0;
        hash += (drugId != null ? drugId.hashCode() : 0);
        return hash;
    }

    @Override
    public boolean equals(Object object) {
        if (!(object instanceof Drug)) {
            return false;
        }
        Drug other = (Drug) object;
        return !((this.drugId == null && other.drugId != null)
                || (this.drugId != null && !this.drugId.equals(other.drugId)));
    }

    @Override
    public String toString() {
        return "com.ttkp.pojo.Drug[ drugId=" + drugId + " ]";
    }
}