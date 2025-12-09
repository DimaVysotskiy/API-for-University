from fastapi import APIRouter, Depends, HTTPException, status
from ..dependencies import get_db
from ..models import RoleInSystem
from ..repositories import StudentInfoRepository, GroupRepository, UserRepository
from ..models.pydantic_models import StudentInfoCreate, StudentInfoUpdate, StudentInfoResponse
from sqlalchemy.ext.asyncio import AsyncSession
from ..core import role_required
from typing import List

student_info_router = APIRouter(prefix="/student-info", tags=["Работа с информацией о студентах в бд."])


@student_info_router.post("/add", response_model=StudentInfoResponse, summary="Добавление информации о студенте.")
async def add_student_info(
    student_data: StudentInfoCreate,
    session: AsyncSession = Depends(get_db),
    _ = Depends(role_required([RoleInSystem.admin, RoleInSystem.teacher]))
):
    """Создание новой записи о студенте. Доступно для администраторов и учителей."""
    student_repo = StudentInfoRepository()
    user_repo = UserRepository()
    group_repo = GroupRepository()
    
    # Проверяем, не существует ли уже информация о студенте для этого пользователя
    if await student_repo.get_by_user_id(session, student_data.user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Student info for user with id {student_data.user_id} already exists"
        )
    
    # Проверяем существование пользователя
    user = await user_repo.get_by_id(session, student_data.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {student_data.user_id} not found"
        )
    
    # Проверяем существование группы
    group = await group_repo.get_by_id(session, student_data.group_id)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group with id {student_data.group_id} not found"
        )
    
    # Проверяем уникальность номера зачетной книжки
    if await student_repo.check_zach_number_exists(session, student_data.zach_number):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Student with zach_number '{student_data.zach_number}' already exists"
        )
    
    try:
        new_student_info = await student_repo.create(
            session=session,
            data=student_data.model_dump()
        )
        return new_student_info
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create student info: {str(e)}"
        )


@student_info_router.get("/{student_info_id}", response_model=StudentInfoResponse, summary="Получение информации о студенте по ID.")
async def get_student_info(
    student_info_id: int,
    session: AsyncSession = Depends(get_db),
    _ = Depends(role_required([RoleInSystem.admin, RoleInSystem.teacher, RoleInSystem.student]))
):
    """Получение информации о студенте по ID. Доступно для всех авторизованных пользователей."""
    student_repo = StudentInfoRepository()
    
    student_info = await student_repo.get_by_id(session, student_info_id)
    if not student_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student info with id {student_info_id} not found"
        )
    return student_info


@student_info_router.get("/user/{user_id}", response_model=StudentInfoResponse, summary="Получение информации о студенте по user_id.")
async def get_student_info_by_user_id(
    user_id: int,
    session: AsyncSession = Depends(get_db),
    _ = Depends(role_required([RoleInSystem.admin, RoleInSystem.teacher, RoleInSystem.student]))
):
    """Получение информации о студенте по user_id. Доступно для всех авторизованных пользователей."""
    student_repo = StudentInfoRepository()
    
    student_info = await student_repo.get_by_user_id(session, user_id)
    if not student_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student info for user with id {user_id} not found"
        )
    return student_info


@student_info_router.get("/group/{group_id}", response_model=List[StudentInfoResponse], summary="Получение списка студентов группы.")
async def get_students_by_group(
    group_id: int,
    session: AsyncSession = Depends(get_db),
    _ = Depends(role_required([RoleInSystem.admin, RoleInSystem.teacher, RoleInSystem.student]))
):
    """Получение списка студентов группы. Доступно для всех авторизованных пользователей."""
    student_repo = StudentInfoRepository()
    group_repo = GroupRepository()
    
    # Проверяем существование группы
    group = await group_repo.get_by_id(session, group_id)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group with id {group_id} not found"
        )
    
    students = await student_repo.get_by_group_id(session, group_id)
    return students


@student_info_router.get("/", response_model=List[StudentInfoResponse], summary="Получение всех студентов.")
async def get_all_students(
    session: AsyncSession = Depends(get_db),
    _ = Depends(role_required([RoleInSystem.admin, RoleInSystem.teacher]))
):
    """Получение списка всех студентов. Доступно для администраторов и учителей."""
    student_repo = StudentInfoRepository()
    
    students = await student_repo.get_all(session)
    return students


@student_info_router.put("/{student_info_id}", response_model=StudentInfoResponse, summary="Обновление информации о студенте.")
async def update_student_info(
    student_info_id: int,
    student_data: StudentInfoUpdate,
    session: AsyncSession = Depends(get_db),
    _ = Depends(role_required([RoleInSystem.admin, RoleInSystem.teacher]))
):
    """Обновление информации о студенте. Доступно для администраторов и учителей."""
    student_repo = StudentInfoRepository()
    group_repo = GroupRepository()
    
    # Проверяем существование записи о студенте
    existing_student = await student_repo.get_by_id(session, student_info_id)
    if not existing_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student info with id {student_info_id} not found"
        )
    
    # Если обновляется group_id, проверяем существование группы
    if student_data.group_id is not None:
        group = await group_repo.get_by_id(session, student_data.group_id)
        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Group with id {student_data.group_id} not found"
            )
    
    # Если обновляется zach_number, проверяем уникальность
    if student_data.zach_number is not None:
        existing_by_zach = await student_repo.get_by_zach_number(session, student_data.zach_number)
        if existing_by_zach and existing_by_zach.id != student_info_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Student with zach_number '{student_data.zach_number}' already exists"
            )
    
    try:
        updated_student = await student_repo.update(
            session=session,
            pk=student_info_id,
            data=student_data.model_dump(exclude_none=True)
        )
        return updated_student
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update student info: {str(e)}"
        )


@student_info_router.delete("/{student_info_id}", summary="Удаление информации о студенте.")
async def delete_student_info(
    student_info_id: int,
    session: AsyncSession = Depends(get_db),
    _ = Depends(role_required([RoleInSystem.admin]))
):
    """Удаление информации о студенте. Доступно только для администраторов."""
    student_repo = StudentInfoRepository()
    
    # Проверяем существование записи о студенте
    existing_student = await student_repo.get_by_id(session, student_info_id)
    if not existing_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student info with id {student_info_id} not found"
        )
    
    try:
        deleted = await student_repo.delete(session, student_info_id)
        if deleted:
            return {"message": f"Student info with id {student_info_id} deleted successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete student info"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete student info: {str(e)}"
        )
