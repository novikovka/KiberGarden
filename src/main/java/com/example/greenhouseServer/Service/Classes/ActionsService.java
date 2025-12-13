package com.example.greenhouseServer.Service.Classes;

import com.example.greenhouseServer.Entity.Actions;
import com.example.greenhouseServer.Entity.CurrentDate;
import com.example.greenhouseServer.Entity.EnumList.TypeBool;
import com.example.greenhouseServer.Entity.Users;
import com.example.greenhouseServer.Repository.ActionsRepositoryIntr;
import com.example.greenhouseServer.Repository.CurrentDateRepositoryIntr;
import com.example.greenhouseServer.Repository.UsersRepositoryIntr;
import com.example.greenhouseServer.Service.Interfaces.ActionsServiceIntr;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import net.javacrumbs.shedlock.spring.annotation.SchedulerLock;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.client.RestTemplate;

import java.time.LocalTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;

@Service
@Transactional(readOnly = true)
@EnableScheduling
public class ActionsService implements ActionsServiceIntr {

    private final ActionsRepositoryIntr actionsRepositoryIntr;

    private final UsersRepositoryIntr usersRepositoryIntr;

    private final CurrentDateRepositoryIntr currentDateRepositoryIntr;

    @Autowired
    public ActionsService(ActionsRepositoryIntr actionsRepositoryIntr, UsersRepositoryIntr usersRepositoryIntr, CurrentDateRepositoryIntr currentDateRepositoryIntr) {
        this.actionsRepositoryIntr = actionsRepositoryIntr;
        this.usersRepositoryIntr = usersRepositoryIntr;
        this.currentDateRepositoryIntr = currentDateRepositoryIntr;
    }

    @Override
    @Transactional
    public void save(Actions actions) {
        Optional<Actions> existingActions = actionsRepositoryIntr.findByTokenAndTypeBool(actions.getToken(), actions.getTypeBool());

        if(existingActions.isPresent()){
            Actions reActions = existingActions.get();
            reActions.setIsWorking(actions.getIsWorking());
            actionsRepositoryIntr.save(reActions);
        } else {
            actionsRepositoryIntr.save(actions);
        }
    }

    @Scheduled(cron = "0 * * * * *")  // каждую минуту
    public void checkTimersEveryMinute() {
        LocalTime currentTime = LocalTime.now();
        System.out.println("Checking timers at: " + currentTime);

        // Получаем только часы и минуты (без секунд)
        LocalTime timeWithoutSeconds = currentTime.withSecond(0).withNano(0);

        getAllTimersActions(timeWithoutSeconds);
    }

    @Transactional
    public void getAllTimersActions(LocalTime time) {
        List<Actions> timerActions = actionsRepositoryIntr.findByTimeAction(time);
        if(!timerActions.isEmpty()) {
            RestTemplate restTemplate = new RestTemplate();
            ObjectMapper objectMapper = new ObjectMapper();
            for (Actions actions : timerActions) {
                try {
                    Map<String, Object> jsonToSend = new HashMap<>();

                    jsonToSend.put("token", actions.getToken());
                    jsonToSend.put("type", actions.getTypeBool());
                    jsonToSend.put("status", actions.getIsWorking());

                    String jsonString = objectMapper.writeValueAsString(jsonToSend);
                    System.out.println("JSON to send: " + jsonString);

                    HttpHeaders headers = new HttpHeaders();
                    headers.setContentType(MediaType.APPLICATION_JSON);

                    HttpEntity<String> request = new HttpEntity<>(jsonString, headers);

                    String url = getUrlUsers(actions.getToken());

                    ResponseEntity<String> response = restTemplate.postForEntity(url, request, String.class);

                    System.out.println("Status: " + response.getStatusCode());
                    System.out.println("Response: " + response.getBody());

                    CurrentDate existingCurrentData = currentDateRepositoryIntr.findByTokenAndTypeBool(actions.getToken(), actions.getTypeBool());
                    if (existingCurrentData != null) {
                        existingCurrentData.setIsWorking(actions.getIsWorking());
                        currentDateRepositoryIntr.save(existingCurrentData);
                        System.out.println(actions.getIsWorking());
                    }
                } catch (Exception e) {
                    System.out.println("Error: " + e.getMessage());
                    e.printStackTrace();
                }
            }
        } else {
            System.out.println("List is empty");
        }
    }

    private String getUrlUsers(String token){
        Users user = usersRepositoryIntr.findByToken(token);
        String ip = user.getIpAddress();
        return "http://" + ip + ":8081/";
    }

}
