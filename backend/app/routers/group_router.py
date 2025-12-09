from fastapi import APIRouter, Depends, HTTPException, status
from ..dependencies import get_db
from ..models import RoleInSystem
from ..repositories import GroupRepository
from ..models.pydantic_models import GroupCreate, GroupUpdate, GroupResponse
from sqlalchemy.ext.asyncio import AsyncSession
from ..core import role_required
from typing import List

group_router = APIRouter(prefix="/group", tags=["Работа с группами в бд."])


@group_router.post("/add", response_model=GroupResponse, summary="Добавление группы.")
async def add_group(
    group_data: GroupCreate,
    session: AsyncSession = Depends(get_db),
    _ = Depends(role_required([RoleInSystem.admin, RoleInSystem.teacher]))
):
    """Создание новой группы. Доступно для администраторов и учителей."""
    group_repo = GroupRepository()
    
    try:
        new_group = await group_repo.create(
            session=session,
            data=group_data.model_dump(exclude_none=True)
        )
        return new_group
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create group: {str(e)}"
        )


@group_router.get("/{group_id}", response_model=GroupResponse, summary="Получение группы по ID.")
async def get_group(
    group_id: int,
    session: AsyncSession = Depends(get_db),
    _ = Depends(role_required([RoleInSystem.admin, RoleInSystem.teacher, RoleInSystem.student]))
):
    """Получение информации о группе по ID. Доступно для всех авторизованных пользователей."""
    group_repo = GroupRepository()
    
    group = await group_repo.get_by_id(session, group_id)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group with id {group_id} not found"
        )
    return group


@group_router.get("/", response_model=List[GroupResponse], summary="Получение всех групп.")
async def get_all_groups(
    session: AsyncSession = Depends(get_db),
    _ = Depends(role_required([RoleInSystem.admin, RoleInSystem.teacher, RoleInSystem.student]))
):
    """Получение списка всех групп. Доступно для всех авторизованных пользователей."""
    group_repo = GroupRepository()
    
    groups = await group_repo.get_all(session)
    return groups


@group_router.put("/{group_id}", response_model=GroupResponse, summary="Обновление группы.")
async def update_group(
    group_id: int,
    group_data: GroupUpdate,
    session: AsyncSession = Depends(get_db),
    _ = Depends(role_required([RoleInSystem.admin, RoleInSystem.teacher]))
):
    """Обновление информации о группе. Доступно для администраторов и учителей."""
    group_repo = GroupRepository()
    
    # Проверяем существование группы
    existing_group = await group_repo.get_by_id(session, group_id)
    if not existing_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group with id {group_id} not found"
        )
    
    try:
        updated_group = await group_repo.update(
            session=session,
            pk=group_id,
            data=group_data.model_dump(exclude_none=True)
        )
        return updated_group
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update group: {str(e)}"
        )


@group_router.delete("/{group_id}", summary="Удаление группы.")
async def delete_group(
    group_id: int,
    session: AsyncSession = Depends(get_db),
    _ = Depends(role_required([RoleInSystem.admin]))
):
    """Удаление группы. Доступно только для администраторов."""
    group_repo = GroupRepository()
    
    # Проверяем существование группы
    existing_group = await group_repo.get_by_id(session, group_id)
    if not existing_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group with id {group_id} not found"
        )
    
    try:
        deleted = await group_repo.delete(session, group_id)
        if deleted:
            return {"message": f"Group with id {group_id} deleted successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete group"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete group: {str(e)}"
        )
