package com.example.greenhouseServer.Controllers;

import com.example.greenhouseServer.Entity.Actions;
import com.example.greenhouseServer.Service.Interfaces.ActionsServiceIntr;
import com.example.greenhouseServer.util.ErrorResponse;
import com.example.greenhouseServer.util.IndicationsNotCreatedException;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.BindingResult;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping("/api")
public class ActionsController {

    private final ActionsServiceIntr actionsServiceIntr;

    @Autowired
    public ActionsController(ActionsServiceIntr actionsServiceIntr) {
        this.actionsServiceIntr = actionsServiceIntr;
    }

    @GetMapping("/createActions")
    public ResponseEntity<HttpStatus> createActions(@RequestBody @Valid Actions actions,
                                                    BindingResult bindingResult){
        if (bindingResult.hasErrors()){
            StringBuilder errorMsg = new StringBuilder();

            List<FieldError> errors = bindingResult.getFieldErrors();
            for(FieldError error : errors){
                errorMsg.append(error.getField())
                        .append(" --- ").append(error.getDefaultMessage())
                        .append(";");
            }

            throw new IndicationsNotCreatedException(errorMsg.toString());
        }

        actionsServiceIntr.save(actions);
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
