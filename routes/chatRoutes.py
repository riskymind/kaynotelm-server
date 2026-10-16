from fastapi import APIRouter, HTTPException, Depends
from services.supabase_service import supabase
from services.auth_service import get_current_user_clerk_id
from models.index import ChatCreate, ChatUpdate


router = APIRouter(tags=["Chat Routes"])

"""
`/api/chats`
    - POST `/` ~ Create a new chat
    - PATCH `/{chat_id}` ~ Update a specific chat
    - DELETE `/{chat_id}` ~ Delete a specific chat

"""


@router.post("/")
async def create_chat(
    chat: ChatCreate, current_user_clerk_id: str = Depends(get_current_user_clerk_id)
):
    """
    ! Logic Flow
    * 1. Get current user clerk_id
    * 2. Insert new chat into database
    * 3. Check if chat creation failed, then return error
    * 4. Return successfully created chat data
    """
    try:
        chat_insert_data = {
            "title": chat.title,
            "project_id": chat.project_id,
            "clerk_id": current_user_clerk_id,
        }
        chat_creation_result = (
            supabase.table("chats").insert(chat_insert_data).execute()
        )

        if not chat_creation_result.data:
            raise HTTPException(
                status_code=422, detail="Failed to create chat - invalid data provided"
            )

        return {
            "message": "Chat created successfully",
            "data": chat_creation_result.data[0],
        }
    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An internal server error occurred while creating chat: {str(e)}",
        )


@router.patch("/{chat_id}")
async def update_chat(
    chat_id: str,
    chat_data: ChatUpdate,
    current_user_clerk_id: str = Depends(get_current_user_clerk_id),
):
    """
    ! Logic Flow
    * 1. Get current user clerk_id
    * 2. Build update payload from provided fields only
    * 3. Update chat if it exists and belongs to the current user
    * 4. Check if chat update failed, then return error
    * 5. Return updated chat data
    """
    try:
        # Build update payload from provided fields only
        chat_update_data = chat_data.model_dump(exclude_unset=True)

        if not chat_update_data:
            raise HTTPException(
                status_code=400,
                detail="No fields provided to update",
            )

        if "title" in chat_update_data and not (chat_update_data["title"] or "").strip():
            raise HTTPException(
                status_code=422,
                detail="Chat title cannot be empty",
            )

        chat_update_result = (
            supabase.table("chats")
            .update(chat_update_data)
            .eq("id", chat_id)
            .eq("clerk_id", current_user_clerk_id)
            .execute()
        )

        if not chat_update_result.data:
            raise HTTPException(
                status_code=404,
                detail="Chat not found or you don't have permission to edit it",
            )

        return {
            "message": "Chat updated successfully",
            "data": chat_update_result.data[0],
        }
    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An internal server error occurred while updating chat {chat_id}: {str(e)}",
        )


@router.delete("/{chat_id}")
async def delete_chat(
    chat_id: str, current_user_clerk_id: str = Depends(get_current_user_clerk_id)
):
    """
    ! Logic Flow
    * 1. Get current user clerk_id
    * 2. Verify if the chat exists and belongs to the current user
    * 3. Delete chat
    * 4. Return successfully deleted chat data
    """
    try:
        chat_deletion_result = (
            supabase.table("chats")
            .delete()
            .eq("id", chat_id)
            .eq("clerk_id", current_user_clerk_id)
            .execute()
        )
        if not chat_deletion_result.data:
            raise HTTPException(
                status_code=404,
                detail="Chat not found or you don't have permission to delete it",
            )

        return {
            "message": "Chat deleted successfully",
            "data": chat_deletion_result.data[0],
        }
    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An internal server error occurred while deleting chat {chat_id}: {str(e)}",
        )
