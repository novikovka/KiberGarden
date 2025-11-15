package com.example.greenhouseServer.Controllers;

import com.example.greenhouseServer.Entity.Notifications;
import com.example.greenhouseServer.Service.Interfaces.NotificationsServiceIntr;
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
public class NotificationsController {

    private final NotificationsServiceIntr notificationsServiceIntr;

    @Autowired
    public NotificationsController(NotificationsServiceIntr notificationsServiceIntr) {
        this.notificationsServiceIntr = notificationsServiceIntr;
    }

    @PostMapping("/createNotification")
    public ResponseEntity<HttpStatus> createNotification(@RequestBody @Valid Notifications notifications,
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
        notificationsServiceIntr.save(notifications);
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
