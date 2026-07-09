package com.ttkp.repositories.impl;

import com.ttkp.hibernatedemomedicare.HibernateUtils;
import com.ttkp.pojo.Drug;
import com.ttkp.repositories.DrugRepository;
import java.util.List;
import org.hibernate.Session;
import org.hibernate.Transaction;

public class DrugRepositoryImpl implements DrugRepository {

    @Override
    public List<Drug> getDrugs() {
        try (Session session = HibernateUtils.getFactory().openSession()) {
            return session.createNamedQuery("Drug.findAll", Drug.class).getResultList();
        }
    }

    @Override
    public Drug getDrugById(int id) {
        try (Session session = HibernateUtils.getFactory().openSession()) {
            return session.get(Drug.class, id);
        }
    }

    @Override
    public boolean addOrUpdateDrug(Drug drug) {
        Transaction tx = null;

        try (Session session = HibernateUtils.getFactory().openSession()) {
            tx = session.beginTransaction();

            if (drug.getDrugId() == null) {
                session.persist(drug);
            } else {
                session.merge(drug);
            }

            tx.commit();
            return true;
        } catch (Exception ex) {
            if (tx != null) {
                tx.rollback();
            }
            ex.printStackTrace();
            return false;
        }
    }

    @Override
    public boolean deleteDrug(int id) {
        Transaction tx = null;

        try (Session session = HibernateUtils.getFactory().openSession()) {
            tx = session.beginTransaction();

            Drug d = session.get(Drug.class, id);
            if (d != null) {
                session.remove(d);
            }

            tx.commit();
            return true;
        } catch (Exception ex) {
            if (tx != null) {
                tx.rollback();
            }
            ex.printStackTrace();
            return false;
        }
    }
}
