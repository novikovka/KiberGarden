package com.example.greenhouseServer.Service.Interfaces;

import com.example.greenhouseServer.Entity.Users;

public interface UsersServiceIntr {
    void save (Users user);
    void update (String token, String ipAddress);
}
