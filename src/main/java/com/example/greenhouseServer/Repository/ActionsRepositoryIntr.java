package com.example.greenhouseServer.Repository;

import com.example.greenhouseServer.Entity.Actions;
import com.example.greenhouseServer.Entity.EnumList.TypeBool;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalTime;
import java.util.List;
import java.util.Optional;

@Repository
public interface ActionsRepositoryIntr extends JpaRepository<Actions, Long> {
    @Query("SELECT a FROM Actions a WHERE a.typeBool != :lastType AND a.idActions = :id")
    Optional<Actions> findIfTypeChanged(@Param("id") Long id, @Param("lastType") TypeBool lastType);

    List<Actions> findByTimeAction(LocalTime time);

    List<Actions> findByIsWorkingTrue();

    Optional<Actions> findByToken(String token);

    Optional<Actions> findByTokenAndTypeBool(String token, TypeBool typeBool);
}
