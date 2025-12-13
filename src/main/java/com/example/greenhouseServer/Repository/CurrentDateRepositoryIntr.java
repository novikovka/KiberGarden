package com.example.greenhouseServer.Repository;

import com.example.greenhouseServer.Entity.CurrentDate;
import com.example.greenhouseServer.Entity.EnumList.TypeBool;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface CurrentDateRepositoryIntr extends JpaRepository<CurrentDate, Long> {
    CurrentDate findByToken(String token);
    CurrentDate findByTokenAndTypeBool(String token, TypeBool type);
}
