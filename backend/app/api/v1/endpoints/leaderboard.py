from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.session import get_db
from app.models.gamification import Leaderboard, Achievement, UserAchievement
from app.models.user import User
from typing import List

router = APIRouter()


@router.get("/leaderboard/weekly")
def get_weekly_leaderboard(
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Get weekly profit leaderboard."""
    leaderboard = db.query(
        Leaderboard, User
    ).join(
        User, Leaderboard.user_id == User.id
    ).filter(
        Leaderboard.period == "weekly"
    ).order_by(
        desc(Leaderboard.weekly_profit)
    ).limit(limit).all()
    
    return [
        {
            "rank": idx + 1,
            "user_id": entry.Leaderboard.user_id,
            "username": entry.User.username,
            "weekly_profit": entry.Leaderboard.weekly_profit
        }
        for idx, entry in enumerate(leaderboard)
    ]


@router.get("/leaderboard/all-time")
def get_all_time_leaderboard(
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Get all-time profit leaderboard."""
    leaderboard = db.query(
        Leaderboard, User
    ).join(
        User, Leaderboard.user_id == User.id
    ).filter(
        Leaderboard.period == "all_time"
    ).order_by(
        desc(Leaderboard.all_time_profit)
    ).limit(limit).all()
    
    return [
        {
            "rank": idx + 1,
            "user_id": entry.Leaderboard.user_id,
            "username": entry.User.username,
            "all_time_profit": entry.Leaderboard.all_time_profit
        }
        for idx, entry in enumerate(leaderboard)
    ]


@router.get("/leaderboard/accuracy")
def get_accuracy_leaderboard(
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Get prediction accuracy leaderboard."""
    leaderboard = db.query(
        Leaderboard, User
    ).join(
        User, Leaderboard.user_id == User.id
    ).filter(
        Leaderboard.period == "all_time"
    ).order_by(
        desc(Leaderboard.prediction_accuracy)
    ).limit(limit).all()
    
    return [
        {
            "rank": idx + 1,
            "user_id": entry.Leaderboard.user_id,
            "username": entry.User.username,
            "prediction_accuracy": entry.Leaderboard.prediction_accuracy
        }
        for idx, entry in enumerate(leaderboard)
    ]


@router.get("/achievements")
def get_all_achievements(db: Session = Depends(get_db)):
    """Get all available achievements."""
    achievements = db.query(Achievement).all()
    
    return [
        {
            "id": achievement.id,
            "name": achievement.name,
            "description": achievement.description,
            "badge_icon": achievement.badge_icon,
            "criteria_type": achievement.criteria_type,
            "criteria_value": achievement.criteria_value
        }
        for achievement in achievements
    ]


@router.get("/achievements/user/{user_id}")
def get_user_achievements(user_id: int, db: Session = Depends(get_db)):
    """Get achievements unlocked by a specific user."""
    user_achievements = db.query(
        UserAchievement, Achievement
    ).join(
        Achievement, UserAchievement.achievement_id == Achievement.id
    ).filter(
        UserAchievement.user_id == user_id
    ).all()
    
    return [
        {
            "achievement_id": entry.Achievement.id,
            "name": entry.Achievement.name,
            "description": entry.Achievement.description,
            "badge_icon": entry.Achievement.badge_icon,
            "unlocked_at": entry.UserAchievement.unlocked_at
        }
        for entry in user_achievements
    ]
