package com.example.greenhouseServer.Service.Classes;

import com.example.greenhouseServer.Entity.Users;
import com.example.greenhouseServer.Repository.UsersRepositoryIntr;
import com.example.greenhouseServer.Service.Interfaces.UsersServiceIntr;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional(readOnly = true)
public class UsersService implements UsersServiceIntr {

    private final UsersRepositoryIntr usersRepositoryIntr;

    @Autowired
    public UsersService(UsersRepositoryIntr usersRepositoryIntr) {
        this.usersRepositoryIntr = usersRepositoryIntr;
    }

    @Override
    @Transactional
    public void save(Users user) {
        usersRepositoryIntr.save(user);
    }
}
