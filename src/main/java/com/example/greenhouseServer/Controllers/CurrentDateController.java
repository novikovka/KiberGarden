package com.example.greenhouseServer.Controllers;

import com.example.greenhouseServer.Entity.CurrentDate;
import com.example.greenhouseServer.Service.Interfaces.CurrentDateServiceIntr;
import com.example.greenhouseServer.util.ErrorResponse;
import com.example.greenhouseServer.util.IndicationsNotCreatedException;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.BindingResult;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api")
public class CurrentDateController {

    private final CurrentDateServiceIntr currentDateServiceIntr;

    @Autowired
    public CurrentDateController(CurrentDateServiceIntr currentDateServiceIntr) {
        this.currentDateServiceIntr = currentDateServiceIntr;
    }

    @PostMapping("/createCurrentDate")
    public ResponseEntity<HttpStatus> createCurrentDate(@RequestBody @Valid CurrentDate currentDate,
                                                        BindingResult bindingResult){
        if(bindingResult.hasErrors()){
            StringBuilder errorMsg = new StringBuilder();

            List<FieldError> errors = bindingResult.getFieldErrors();
            for(FieldError error : errors){
                errorMsg.append(error.getField())
                        .append(" --- ").append(error.getDefaultMessage())
                        .append(";");
            }
            throw new IndicationsNotCreatedException(errorMsg.toString());
        }

        currentDateServiceIntr.save(currentDate);
        return ResponseEntity.ok(HttpStatus.OK);
    }

    @ExceptionHandler
    private ResponseEntity<ErrorResponse> handlerException(IndicationsNotCreatedException e){
        ErrorResponse errorResponse = new ErrorResponse(
                e.getMessage(),
                System.currentTimeMillis()
        );

        return new ResponseEntity<>(errorResponse, HttpStatus.BAD_REQUEST);
    }

}
