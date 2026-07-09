package com.ttkp.controllers;

import com.ttkp.pojo.Drug;
import com.ttkp.services.DrugService;
import java.util.List;
import java.util.Map;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;

@RestController
@RequestMapping("/api")
@CrossOrigin
public class ApiDrugController {

    @Autowired
    private DrugService drugService;

    @GetMapping("/drugs")
    public ResponseEntity<List<Drug>> list(@RequestParam Map<String, String> params) {
        return new ResponseEntity<>(this.drugService.getDrugs(params), HttpStatus.OK);
    }

    @GetMapping("/drugs/{id}")
    public ResponseEntity<Drug> retrieve(@PathVariable("id") int id) {
        Drug d = this.drugService.getDrugById(id);

        if (d == null) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

        return new ResponseEntity<>(d, HttpStatus.OK);
    }

    @PostMapping("/drugs")
    public ResponseEntity<?> create(
            @RequestBody Drug drug) {

        boolean success
                = this.drugService.addOrUpdateDrug(drug);

        if (!success) {
            return new ResponseEntity<>(
                    "Không thể thêm thuốc",
                    HttpStatus.BAD_REQUEST);
        }

        return new ResponseEntity<>(
                drug,
                HttpStatus.CREATED);
    }

    @PutMapping("/drugs/{id}")
    public ResponseEntity<?> update(
            @PathVariable("id") int id,
            @RequestBody Drug drug) {

        Drug current
                = this.drugService.getDrugById(id);

        if (current == null) {
            return new ResponseEntity<>(
                    HttpStatus.NOT_FOUND);
        }

        drug.setDrugId(id);

        boolean success
                = this.drugService.addOrUpdateDrug(drug);

        if (!success) {
            return new ResponseEntity<>(
                    "Không thể cập nhật thuốc",
                    HttpStatus.BAD_REQUEST);
        }

        return new ResponseEntity<>(
                drug,
                HttpStatus.OK);
    }

    @DeleteMapping("/drugs/{id}")
    public ResponseEntity<?> delete(
            @PathVariable("id") int id) {

        boolean success
                = this.drugService.deleteDrug(id);

        if (!success) {
            return new ResponseEntity<>(
                    HttpStatus.NOT_FOUND);
        }

        return new ResponseEntity<>(
                HttpStatus.NO_CONTENT);
    }

    @GetMapping("/statistics/drugs-total")
    public ResponseEntity<Long> countDrugs() {
        return new ResponseEntity<>(
                this.drugService.countDrugs(),
                HttpStatus.OK
        );
    }

    @GetMapping("/statistics/drugs-by-category")
    public ResponseEntity<List<Object[]>> countDrugsByCategory() {
        return new ResponseEntity<>(
                this.drugService.countDrugsByCategory(),
                HttpStatus.OK
        );
    }
}
